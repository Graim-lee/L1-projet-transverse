""" InputsManager.py
    Manage inputs
"""
import pygame
import Scripts.Object as Object
import Scripts.Constants as Constants

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

def CheckInputs() -> bool:
    """ Main function, checks every input. If you want to detect an input, place the code here.
        Returns :
            - (bool): True if the game is running, False otherwise. Allows main.py to know if the game should end.
            - (string): The direction to go
    """
    global pressingQA, pressingD, slingshotArmed, slingshotStart

    # Every event.
    for event in pygame.event.get():

        # KEYDOWN = the user just pressed a key (only happens the first frame after the user presses said key).
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN: return False   # 'Enter' = fin du jeu.
            elif event.key == pygame.K_ESCAPE: PressEscape()              # 'Escape' = menu différent.
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

        # KEYUP = the user just released a key (only happens on the first frame after releasing the key).
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_SPACE: PlayerReleaseJump()     # Slows down the jump when the player releases the key.

            elif event.key == pygame.K_a: 
                pressingQA = False   # 'A'
            elif event.key == pygame.K_q:
                pressingQA = False   # 'Q'
            elif event.key == pygame.K_d:
                pressingD = False   # 'D'

        # 'Left-click' = slingshot
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            slingshotArmed = True
            mouseX, mouseY = pygame.mouse.get_pos()
            slingshotStart = Object.Vector2(mouseX, mouseY)
            DisplayDots()

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            slingshotArmed = False
            UseSlingshot()
            HideDots()

    ApplyInputs()   # We apply the inputs' effects.
    return True

def ApplyInputs():
    """ After retrieving every input, this function applies the inputs' effects, such as moving the character. """
    global jumpBufferTimer, slingshotArmed

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

    # Prevents the player from jumping midair.
    if not player.grounded: return

    # Computes the force of propulsion.
    mousePos = Object.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    propulsionForce = (slingshotStart - mousePos) * Constants.slingshotForce

    #print(propulsionForce)

    """if xDiff < -1.5: xDiff = -1.5
    elif xDiff > 1.5: xDiff = 1.5
    if yDiff < -1.5: yDiff = -1.5
    elif yDiff > 1.5: yDiff = 1.5"""

    # Application of the force.
    player.instantVelocity += propulsionForce

def ShowSlingshotTrajectory():
    global slingshotStart

    # Initial conditions : x0 is the position of the player ; v0 is the initial speed of the player (given by the
    # slingshot vector). I must specify the type of x0 else my IDE gives me a warning, and it annoys me :'(
    x0: Object.Vector2 = (player.position + 0.5 * player.size) * (2.0 / Constants.G)
    v0 = (slingshotStart - Object.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])) * Constants.slingshotForce

    """if v0.x > 1.5: v0.x = 1.5
    elif v0.x < -1.5: v0.x = -1.5
    if v0.y > 1.5: v0.y = 1.5
    elif v0.y < -1.5: v0.y = -1.5"""

    # The trajectory equation is x(t) = v0 * t - 0.5 * g * (t^3 / 3 + t^2 / 2 + x0).
    dotsPosition = []
    for t in range(1, 6):
        timeSplit = t * 0.2     # Time between two dots.
        framesCount = timeSplit * Constants.framerate   # Number of frames elapsed in the range of timeSplit.
        pos = timeSplit * v0 + timeSplit * 0.5 * Constants.G * Object.Vector2(0, framesCount * (framesCount + 1)) + x0
        print("Position : " + str(pos))
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
            newDot = Object.GameObject((0, 0), (10 - i, 10 - i), "Sprites/dot.png", 0, 2, [0, 1, 2], "Level_0")
            mainPooler.AddObject(newDot, "Trajectory")

    for dot in mainPooler.main["Trajectory"]:
        dot.active = True

def HideDots():
    global mainPooler

    for dot in mainPooler.main["Trajectory"]:
        dot.active = False