""" InputsManager.py
    Manage inputs
"""
import pygame
import math
import Scripts.Object as Object
import Scripts.Constants as Constants
import Scripts.Physics as Physics

mainPooler = Object.Pooler({})
player: Object.GameObject

pressingQA = False
pressingD = False
slingshotArmed = False
slingshotStart = Object.Vector2(0, 0)

jumpBufferTimer = 0     # Allows the player to press 'Space' a little before actually landing, and still jump.

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
            elif event.key == pygame.K_SPACE: StartJumpBufferTimer()     # 'Space' = jump (start of the jump buffer timer).

            # For most of the inputs, we want to know if they are being pressed continuously, and not only on the exact
            # frame they were pressed. To achieve that, when a key is pressed, we switch its bool value (i.e.: pressingA)
            # to True, and put it back to False when we detect that the user released the key.

            elif event.key == pygame.K_a:
                pressingQA = True  # 'A'
                player.moving = -1
            elif event.key == pygame.K_q:
                pressingQA = True  # 'Q'
                player.moving = -1
            elif event.key == pygame.K_d:
                pressingD = True  # 'D'
                player.moving = 1

        """ KEYUP ======================================================================================================
        The user just released a key (only happens on the first frame after releasing the key) ===================== """
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_SPACE: PlayerReleaseJump()     # Slows down the jump when the player releases the key.

            elif event.key == pygame.K_a:
                pressingQA = False   # 'A'
            elif event.key == pygame.K_q:
                pressingQA = False   # 'Q'
            elif event.key == pygame.K_d:
                pressingD = False   # 'D'

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
                    for button in mainPooler.main["Button"]:
                        # We check for each button if it is in the desired range.
                        if not button.active: continue
                        if button.scene != Constants.currentScene: continue
                        if button.position.x > mouseX or button.position.x + Constants.buttonSize[0] < mouseX: continue
                        if button.position.y > mouseY or button.position.y + Constants.buttonSize[1] < mouseY: continue
                        button.data[1]()    # We call the function associated to the button.
            if event.button == 3:
                slingshotArmed = False
                HideDots()

        """ LEFT-CLICK RELEASED ========================================================================================
        When the user lets go of left-click ======================================================================== """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if slingshotArmed:
                UseSlingshot()
                HideDots()
            slingshotArmed = False

        if event.type == pygame.K_z: continue

    ApplyInputs()   # We apply the inputs' effects.


""" ================================================================================================================ """


def ApplyInputs():
    """ After retrieving every input, this function applies the inputs' effects, such as moving the character. """
    global jumpBufferTimer, slingshotArmed
    if player.grounded:
        if pressingQA: MovePlayer(-1)    # 'A' or 'Q'
        if pressingD: MovePlayer(1)     # 'D'

    if not pressingQA and not pressingD: player.moving = 0

    if jumpBufferTimer > 0:
        JumpPlayer()    # 'Space'
        jumpBufferTimer -= Constants.deltaTime
    
    if slingshotArmed: ShowSlingshotTrajectory()

def MovePlayer(direction: int):
    """ When the user presses 'A' or 'D'. Makes the player go left or right (depending on the parameter direction) by
    applying a left/rightward velocity to it. Also prevents the player from exceeding a certain maximum speed. Using
    moveVelocity allows to cancel the movement when detecting a collision (so that the player can't phase through walls).
        Args :
            - direction (int): only takes in 1 or -1. Determines whether the player should move right or left.
    """
    # Prevents the player from exceeding the maximum speed.
    if Sign(direction * Constants.maxPlayerSpeed - player.continuousVelocity.x) != Sign(direction): return True
    # Increases the velocity of the player.
    player.continuousVelocity += Object.Vector2(direction * Constants.playerSpeed, 0) * Constants.deltaTime

def StartJumpBufferTimer():
    """ Sets the jumpBufferTimer to a constant. While the jump buffer timer is active (that is, greater than 0), the
    player will jump as soon as he is grounded. """
    global jumpBufferTimer
    jumpBufferTimer = Constants.maxJumpBufferTimer

def PressEscape():
    """ Is executed when the player pressing 'Escape'. """
    # Switching between the Pause Menu and the Game.
    if "Level" in Constants.currentScene:
        Constants.currentLevel = Constants.currentScene
        Constants.currentScene = "Pause_Menu"

    elif Constants.currentScene == "Pause_Menu":
        Constants.currentScene = Constants.currentLevel

def JumpPlayer():
    """ Applies an upward velocity to the player for it to jump. """
    global jumpBufferTimer
    if player.grounded:
        player.instantVelocity += Object.Vector2(0, Constants.playerJumpForce) * Constants.deltaTime
        jumpBufferTimer = 0

def PlayerReleaseJump():
    """ Slows down the y velocity of the player when the user releases the 'Space' key. This helps the user by leaving
    him more control over the height of the jump (quickly pressing 'Space' = short jump, long press = high jump). """
    if player.instantVelocity.y < 0:
        player.instantVelocity.y *= Constants.playerStopJumpCoeff

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

    # Resets the jump (= slingshot) count of the player.
    if player.grounded: Constants.playerJumpCount = Constants.maxPlayerJumpCount

    # Prevents the player from jumping midair.
    if Constants.playerJumpCount <= 0: return

    # Computes the force of propulsion.
    mousePos = Object.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    propulsionForce = (slingshotStart - mousePos) * Constants.slingshotForce

    # We limit the force of the slingshot for it not to be too strong.
    if propulsionForce.x ** 2 + propulsionForce.y ** 2 > Constants.maxSlingshotForce ** 2:
        reductionCoeff = Constants.maxSlingshotForce / math.sqrt(propulsionForce.x ** 2 + propulsionForce.y ** 2)
        propulsionForce *= reductionCoeff

    # Application of the force.
    player.instantVelocity = propulsionForce
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

    # The trajectory equation is x(t) = x0 + v0*t*sV - sG*g*t^sGP.
    dotsPosition = []
    for t in range(1, 6):
        timeSplit = t     # Time between two dots.
        pos = x0 + timeSplit * v0 * sV + sG * Constants.G * Object.Vector2(0, timeSplit ** sGP)
        dotsPosition.append(pos)

    # Showing the dots.
    for i in range(5):
        currentDot = mainPooler.main["Trajectory"][i]
        currentDot.position = dotsPosition[i] - 0.5 * currentDot.size
        currentDot.active = True

def DisplayDots():
    global mainPooler

    if len(mainPooler.main["Trajectory"]) == 0:
        for i in range(5):
            newDot = Object.GameObject((0, 0), (10 - i, 10 - i), Constants.currentLevel, "Real", "Sprites/dot.png", 0, 0, [0, 1, 2])
            mainPooler.AddObject(newDot, "Trajectory")

    for dot in mainPooler.main["Trajectory"]:
        dot.active = True

def HideDots():
    global mainPooler

    for dot in mainPooler.main["Trajectory"]:
        dot.active = False