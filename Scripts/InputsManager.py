""" InputsManager.py
    Manage inputs
"""
import pygame
import math
import Scripts.Object as Object
import Scripts.Constants as Constants

mainPooler = Object.Pooler({})
player: Object.GameObject

pressingA = False
pressingD = False

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
    """
    global pressingA, pressingD
    # Every event.
    for event in pygame.event.get():

        # KEYDOWN = the user just pressed a key (only happens the first frame after the user presses said key).
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE: return False   # 'Escape' = end of the game.
            elif event.key == pygame.K_SPACE: JumpPlayer()

            # For most of the inputs, we want to know if they are being pressed continuously, and not only on the exact
            # frame they were pressed. To achieve that, when a key is pressed, we switch its bool value (i.e.: pressingA)
            # to True, and put it back to False when we detect that the user released the key.

            elif event.key == pygame.K_a: pressingA = True  # 'A'
            elif event.key == pygame.K_d: pressingD = True  # 'D'

        # KEYUP = the user just released a key (only happens on the first frame after releasing the key).
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_a: pressingA = False   # 'A'
            if event.key == pygame.K_d: pressingD = False   # 'D'

    ApplyInputs()   # We apply the inputs' effects.
    return True

def ApplyInputs():
    """ After retrieving every input, this function applies the inputs' effects, such as moving the character. """

    if pressingA: MovePlayer(-1)    # 'A'
    if pressingD: MovePlayer(1)     # 'D'

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

def MovePlayer(direction: int):
    """ When the user presses 'A' or 'D'. Makes the player go left or right (depending on the parameter direction) by
    applying a left/rightward velocity to it. Also prevents the player from exceeding a certain maximum speed.
        Args :
            - direction (int): only takes in 1 or -1. Determines whether the player should move right or left.
    """
    # Prevents the player from exceeding the maximum speed.
    if Sign(direction * Constants.maxPlayerSpeed - player.velocity.x) != Sign(direction): return True
    # Increases the velocity of the player.
    player.velocity += Object.Vector2(direction * Constants.playerSpeed, 0) * Constants.deltaTime

def JumpPlayer():
    """ Applies an upward velocity to the player for it to jump. """
    if player.grounded:
        player.velocity += Object.Vector2(0, -10) * Constants.deltaTime