""" InputsManager.py
    Manage inputs
"""
import pygame
import math
import Scripts.Object as Object
import Scripts.Constants as Constants
import Scripts.ButtonFunctions as ButtonFunctions
import Scripts.Physics as Physics

mainPooler = Object.Pooler()
player: Object.GameObject

pressingQA = False
pressingD = False
slingshotArmed = False
slingshotStart = Object.Vector2(0, 0)

def SetPooler(pooler: Object.Pooler):
    """ Allows to retrieve and copy the pooler from main.py. As the Pooler object is mutable (just like lists),
    modifying the main.py pooler will directly modify this one too. This pooler is useful to move objects according to
    user inputs.
        Args :
            - pooler (Pooler): the main.py pooler.
    """
    global mainPooler
    mainPooler = pooler

def SetPlayer(playerChar: Object.GameObject):
    """ Allows to retrieve and copy the player GameObject from main.py. Also mutable, so it will be shared directly
    with the main.py script. Useful as the player is often used in this script.
        Args :
            - playerChar (GameObject): the player GameObject created in main.py.
    """
    global player
    player = playerChar

def ObjectsOverlap(object1: Object.GameObject, object2: Object.GameObject) -> bool:
    """ Returns True if the two objects collide (or overlap), False otherwise. Useful for detecting when the player is at
    a door or on a coin.
        Args:
            - object1 (GameObject): the first object.
            - object2 (GameObject): the second object.
        Returns:
            - (bool): whether the two objects overlap.
    """
    if object2.position.x + object2.size.x < object1.position.x or object2.position.x > object1.position.x + object1.size.x: return False
    if object2.position.y + object2.size.y < object1.position.y or object2.position.y > object1.position.y + object1.size.y: return False
    return True

def CheckInputs():
    """ Main function, checks every input. If you want to detect an input, place the code here. """
    global pressingQA, pressingD, slingshotArmed, slingshotStart
    # We check whether we are in a menu or not.
    Constants.inMenu = "Level" not in Constants.currentScene

    # Every event.
    for event in pygame.event.get():

        """ KEYDOWN ====================================================================================================
        The user just pressed a key (only happens the first frame after the user presses said key) ================= """
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_BACKSPACE: Constants.gameRunning = False   # Backspace = quit game (for debug).
            elif event.key == pygame.K_ESCAPE: PressEscape()              # 'Escape' = different menu.
            elif event.key == pygame.K_z:          # 'Enter' = interact with a door.
                for door in Constants.objectsInScene["Door"]:
                    if not door.active: continue
                    if not ObjectsOverlap(player, door): continue
                    if Constants.currentLevel == "Level_2_2" and Constants.coin_counter < 15 : continue
                    if Constants.currentLevel == "Level 3_1" and Constants.coin_counter < 4 : continue
                    door.data[1]()
                    Constants.groundedFrictionCoeff = 0.7
                    break

            # For most of the inputs, we want to know if they are being pressed continuously, and not only on the exact
            # frame they were pressed. To achieve that, when a key is pressed, we switch its bool value (i.e.: pressingA)
            # to True, and put it back to False when we detect that the user released the key.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                pressingQA = True  # 'A'
            elif event.key == pygame.K_q:
                pressingQA = True  # 'Q'
            elif event.key == pygame.K_d:
                pressingD = True  # 'D'
            elif event.key == pygame.K_s:
                Constants.playerSquishing = True

        """ KEYUP ======================================================================================================
        The user just released a key (only happens on the first frame after releasing the key) ===================== """
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_a:
                pressingQA = False   # 'A'
            elif event.key == pygame.K_q:
                pressingQA = False   # 'Q'
            elif event.key == pygame.K_d:
                pressingD = False   # 'D'
            elif event.key == pygame.K_s:
                Constants.playerSquishing = False

        """ LEFT-CLICK PRESSED =========================================================================================
        Activates right after the user presses left-click ========================================================== """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # If we are playing, we use the slingshot.
                if not Constants.inMenu:
                    slingshotArmed = True
                    mouseX, mouseY = pygame.mouse.get_pos()
                    slingshotStart = Object.Vector2(mouseX, mouseY)
                    DisplayDots()
                # If we are in a menu, we click on a button.
                else:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    for button in Constants.objectsInScene["Button"]:
                        # We check for each button if it is in the desired range.
                        if not button.active: continue
                        if button.position.x - 0.5 * button.size.x > mouseX or button.position.x + 0.5 * button.size.x < mouseX: continue
                        if button.position.y - 0.5 * button.size.y > mouseY or button.position.y + button.size.y < mouseY: continue
                        button.data[1]()    # We call the function associated to the button.
                        break   # Top prevent clicking on multiple buttons on the same frame.

            if event.button == 3:
                slingshotArmed = False
                HideDots()

        """ LEFT-CLICK RELEASED ========================================================================================
        When the user lets go of left-click ======================================================================== """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if slingshotArmed:
                if Constants.heldItem is None: UseSlingshot()
                else: ThrowObject()
                HideDots()
            slingshotArmed = False

        if event.type == pygame.K_z: continue

    """ ANYTIME ========================================================================================================
    The code here executes on each frame, no matter the inputs ===================================================== """
    """ Coin detection """
    for coin in mainPooler.main[Constants.currentScene]["Coin"]:
        if not coin.active : continue
        if coin.position.x - 1.4 * coin.size.x > player.position.x or coin.position.x + 0.9 * coin.size.x < player.position.x: continue
        if coin.position.y - coin.size.y > player.position.y or coin.position.y + coin.size.y < player.position.y: continue
        Constants.coin_counter += 1
        ButtonFunctions.UpdateCoin()
        coin.active = False

    # Throwable object detection.
    if Constants.heldItem is None and Constants.itemThrowTimer <= 0:
        for throwable in Constants.objectsInScene["Throwable"]:
            if not throwable.active: continue
            if not ObjectsOverlap(player, throwable): continue
            Constants.heldItem = throwable
            break

    if Constants.heldItem is not None:
        itemPos = player.position + 0.5 * Object.Vector2(player.size.x, 0) - 0.5 * Constants.heldItem.size
        Constants.heldItem.position = itemPos
        Constants.heldItem.gravity = 0
        Constants.heldItem.instantVelocity = Object.Vector2(0, 0)

    if Constants.itemThrowTimer > 0: Constants.itemThrowTimer -= 1

    ApplyInputs()   # We apply the inputs' effects.


""" ================================================================================================================ """


def ApplyInputs():
    """ After retrieving every input, this function applies the inputs' effects, such as moving the character. """
    global slingshotArmed
    if player.grounded:
        Constants.playerInputDirection = 0
        if pressingQA: Constants.playerInputDirection -= 1    # 'A' or 'Q'
        if pressingD: Constants.playerInputDirection += 1     # 'D'
        if Constants.playerInputDirection != 0: MovePlayer(Constants.playerInputDirection)
        Constants.playerDirection = Constants.playerInputDirection

    if slingshotArmed: ShowSlingshotTrajectory()

def MovePlayer(direction: int):
    """ When the user presses 'A' or 'D'. Makes the player go left or right (depending on the parameter direction) by
    applying a left/rightward velocity to it. Also prevents the player from exceeding a certain maximum speed. Using
    moveVelocity allows to cancel the movement when detecting a collision (so that the player can't phase through walls).
        Args :
            - direction (int): only takes in 1 or -1. Determines whether the player should move right or left.
    """
    # Prevents the player from exceeding the maximum speed.
    if Sign(direction * Constants.maxPlayerSpeed - player.velocity.x) != Sign(direction): return True
    # Increases the velocity of the player.
    if not player.velocity.y:
        player.velocity += Object.Vector2(direction * Constants.playerSpeed, 0) * Constants.deltaTime

def PressEscape():
    """ Is executed when the player pressing 'Escape'. """
    # Switching between the Pause Menu and the Game.
    if "Level" in Constants.currentScene:
        Constants.currentLevel = Constants.currentScene
        Constants.currentScene = "Pause_Menu"

    elif Constants.currentScene == "Pause_Menu":
        Constants.currentScene = Constants.currentLevel

def Sign(x: float) -> int:
    """ Computes the sign of x.
        Args :
            - x (float): the number which sign we want.
        Returns :
            - (int): -1 if x is negative, 1 if x is positive, and 0 if x is null.
    """
    if x < 0: return -1
    if x > 0: return 1
    return 0

def UseSlingshot():
    global slingshotStart

    # Prevents the player from jumping midair.
    if Constants.playerJumpCount <= 0: return

    # Computes the force of propulsion.
    mousePos = Object.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    propulsionForce = (slingshotStart - mousePos) * Constants.slingshotForce

    if mousePos.x < slingshotStart.x:
        Constants.playerDirection = 1
    else:
        Constants.playerDirection = -1

    # We limit the force of the slingshot for it not to be too strong.
    if propulsionForce.x ** 2 + propulsionForce.y ** 2 > Constants.maxSlingshotForce ** 2:
        reductionCoeff = Constants.maxSlingshotForce / math.sqrt(propulsionForce.x ** 2 + propulsionForce.y ** 2)
        propulsionForce *= reductionCoeff

    # Application of the force.
    player.velocity = propulsionForce
    player.gravity = 0
    Constants.playerUsedSlingshot = True
    Constants.playerJumpCount -= 1

def ShowSlingshotTrajectory():
    global slingshotStart

    # Initial conditions : x0 is the position of the player ; v0 is the initial speed of the player (given by the
    # slingshot vector). I must specify the type of x0 else my IDE gives me a warning, and it annoys me :'(
    x0: Object.Vector2 = (player.position + 0.5 * player.size)
    v0 = (slingshotStart - Object.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])) * Constants.slingshotForce

    # We limit the force of the slingshot for it not to be too strong.
    if v0.x**2 + v0.y**2 > Constants.maxSlingshotForce**2:
        reductionCoeff = Constants.maxSlingshotForce / math.sqrt(v0.x ** 2 + v0.y ** 2)
        v0 *= reductionCoeff

    # The three magical constants to display the trajectory (found by trial and error).
    sV, sG, sGP = Constants.slVelocityFactor, Constants.slGravityFactor, Constants.slGravityPower
    m = player.mass if Constants.heldItem is None else Constants.heldItem.mass

    # The trajectory equation is x(t) = x0 + v0*t*sV - sG*g*t^sGP.
    dotsPosition = []
    for t in range(1, 6):
        timeSplit = t * 0.8 / m     # Time between two dots.
        pos = x0 + timeSplit * v0 * sV + m * sG * Constants.G * Object.Vector2(0, timeSplit ** sGP)
        dotsPosition.append(pos)

    # Showing the dots.
    for i in range(5):
        currentDot = mainPooler.main["Level_All"]["Trajectory"][i]
        currentDot.position = dotsPosition[i] - 0.5 * currentDot.size
        currentDot.active = True

def DisplayDots():
    global mainPooler
    for dot in mainPooler.main["Level_All"]["Trajectory"]:
        dot.active = True

def HideDots():
    global mainPooler
    for dot in mainPooler.main["Level_All"]["Trajectory"]:
        dot.active = False

def ThrowObject():
    global slingshotStart

    # Computes the force of propulsion.
    mousePos = Object.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    propulsionForce = (slingshotStart - mousePos) * Constants.slingshotForce

    # We limit the force of the slingshot for it not to be too strong.
    if propulsionForce.x ** 2 + propulsionForce.y ** 2 > Constants.maxSlingshotForce ** 2:
        reductionCoeff = Constants.maxSlingshotForce / math.sqrt(propulsionForce.x ** 2 + propulsionForce.y ** 2)
        propulsionForce *= reductionCoeff

    # Application of the force.
    Constants.heldItem.velocity = propulsionForce
    Constants.heldItem.gravity = 0
    Constants.heldItem = None

    # We reset the cooldown to prevent the player from picking up the item directly after throwing it.
    Constants.itemThrowTimer = Constants.itemThrowCooldown