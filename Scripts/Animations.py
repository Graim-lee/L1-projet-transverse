import pygame
import Scripts.Object as Object
import Scripts.Constants as Constants

playerWalkFrame = 0
playerWalkSprite = 0
playerSpriteFlipped = False
playerPreviousDirection = 1

waterFrame = 0
waterSprite = 0

def AnimatePlayer(player: Object.GameObject):
    """ Sets the right sprite for the player and manages its animations.
        Args:
            - player (GameObject): the player.
    """
    global playerWalkFrame, playerWalkSprite, playerSpriteFlipped, playerPreviousDirection

    if Constants.playerMovingDirection == 0:

        # Idle animation.
        if not Constants.playerSquishing:
            player.SetSprite("Sprites/Player/"+Constants.skin+"/idle.png", True)

        # Squishing animation.
        else:
            player.SetSprite("Sprites/Player/"+Constants.skin+"/squish_1.png", True)

    # Walk animation.
    else:
        playerPreviousDirection = Constants.playerMovingDirection
        playerWalkFrame += 1

        # Changes the animation frame.
        if playerWalkFrame > Constants.playerWalkDuration:
            playerWalkFrame = 0
            playerWalkSprite += 1
            playerWalkSprite %= 2
            if not Constants.playerSquishing: player.SetSprite("Sprites/Player/"+Constants.skin+"/move_" + str(playerWalkSprite + 1)+".png", True)
            else: player.SetSprite("Sprites/Player/"+Constants.skin+"/squish_" + str(playerWalkSprite + 1)+".png", True)

    # Makes the player face the right direction.
    if playerPreviousDirection == -1 and not Constants.playerSpriteFlipped:
        player.surface = pygame.transform.flip(player.surface, True, False)
        Constants.playerSpriteFlipped = True

    player.Resize((44, 44))

def AnimateWater(water: [Object.GameObject]):
    """ Sets the right sprite for every water object and manages their animations.
            Args:
                - water ([GameObject]): the water game object.
    """
    global waterFrame, waterSprite

    waterFrame += 1
    if waterFrame >= Constants.waterAnimDuration:
        waterFrame = 0
        waterSprite += 1
        waterSprite %= 3
        for wat in water:
            wat.SetSprite("Sprites/Water/water_" + str(waterSprite + 1) + ".png", True)
            wat.Resize(wat.size.Tuple())