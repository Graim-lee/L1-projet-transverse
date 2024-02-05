""" InputsManager.py
    Manage inputs
"""
import pygame
import math
import Scripts.Object as Object
import Scripts.Constants as Constants

mainPooler = Object.Pooler({})
player: Object.GameObject

pressingQA = False
pressingD = False
slingshotArmed = False

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

move = [False,"Right"] # [if moving, direction] (jai pas réussi a la mettre dans la fonction CheckInput et la faire changer a chaque fois)
def CheckInputs() -> bool:
    """ Main function, checks every input. If you want to detect an input, place the code here.
        Returns :
            - (bool): True if the game is running, False otherwise. Allows main.py to know if the game should end.
            - (string): The direction to go
    """
    global pressingQA, pressingD, move, slingshotArmed

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

            elif event.key == pygame.K_a: pressingQA = True  # 'A'
            elif event.key == pygame.K_q:
                pressingQA = True  # 'Q'
                move[1] = "Left"  # set the direction to left
                move[0] = True
            elif event.key == pygame.K_d:
                pressingD = True  # 'D'
                move[1] = "Right" # set the direction to right
                move[0] = True


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: slingshotArmed = True

        # KEYUP = the user just released a key (only happens on the first frame after releasing the key).
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_SPACE: PlayerReleaseJump()     # Slows down the jump when the player releases the key.

            elif event.key == pygame.K_a: 
                pressingQA = False   # 'A'
                move[0] = False
            elif event.key == pygame.K_q: 
                pressingQA = False   # 'Q'
                move[0] = False
            elif event.key == pygame.K_d: 
                pressingD = False   # 'D'
                move[0] = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: slingshotArmed = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: 
                slingshotArmed = False
                shooting()


    ApplyInputs()   # We apply the inputs' effects.
    return True, move

def ApplyInputs():
    """ After retrieving every input, this function applies the inputs' effects, such as moving the character. """
    global jumpBufferTimer, slingshotArmed

    if pressingQA: MovePlayer(-1)    # 'A' or 'Q'
    if pressingD: MovePlayer(1)     # 'D'

    if jumpBufferTimer > 0:
        JumpPlayer()    # 'Space'
        jumpBufferTimer -= Constants.deltaTime
    
    if slingshotArmed: Arming()

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
    if Constants.currentScene == 0: Constants.currentScene = 1
    elif Constants.currentScene == 1: Constants.currentScene = 0

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

def Arming():
    mousePos = pygame.mouse.get_pos()
    # print(mousePos, player.position)

def shooting():
    mousePos = pygame.mouse.get_pos()
    xDiff = (player.position.x-mousePos[0])/100
    yDiff = (player.position.y-mousePos[1])/100
    if xDiff < -1.5: xDiff = -1.5
    elif xDiff > 1.5: xDiff = 1.5
    if yDiff < -1.5: yDiff = -1.5
    if player.grounded:
        player.instantVelocity += Object.Vector2(xDiff, yDiff)