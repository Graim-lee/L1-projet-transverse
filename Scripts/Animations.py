import pygame
import Scripts.Object as Object
import Scripts.Constants as Constants

playerWalkFrame = 0
playerWalkSprite = 0

waterFrame = 0
waterSprite = 0
playerSize = 0

def AnimatePlayer(player: Object.GameObject):
    """ Sets the right sprite for the player and manages its animations.
        Args:
            - player (GameObject): the player.
    """
    global playerWalkFrame, playerWalkSprite

    # Direction.
    if (player.velocity.x <0) or (Constants.playerSpriteFlipped and player.velocity.x == 0): playerDirection = True
    else: playerDirection = False

    # Find if we have a special animation because of the world.
    if Constants.currentWorld == "World_2": Constants.playerSpecial = True

    # Animation not moving.
    if player.velocity.x == 0 and Constants.playerGrounded:
        # Idle animation.
        if not Constants.playerSquishing:
            player.SetSprite("Sprites/Player/" + Constants.skin + "/idle.png", playerDirection)

        # Squishing animation.
        else:
            player.SetSprite("Sprites/Player/" + Constants.skin + "/squish_1.png", playerDirection)

    # Fly animation.
    elif not Constants.playerGrounded:
        if player.velocity.y < 0: player.SetSprite("Sprites/Player/" + Constants.skin + "/up.png", playerDirection)
        else: player.SetSprite("Sprites/Player/" + Constants.skin + "/fall.png", playerDirection)

    # Walk animation.
    else :
        playerPreviousDirection = Constants.playerDirection
        playerWalkFrame += 1

        # Changes the animation frame.
        if playerWalkFrame > Constants.playerWalkDuration and abs(player.velocity.x) >= 10 and not Constants.playerSpecial:
            playerWalkFrame = 0
            playerWalkSprite += 1
            playerWalkSprite %= 2
            animType = "/squish_" if Constants.playerSquishing else "/move_"
            player.SetSprite("Sprites/Player/" + Constants.skin + animType + str(playerWalkSprite + 1) + ".png", playerDirection)

        elif Constants.currentWorld == "World_2":
            player.SetSprite("Sprites/Player/" + Constants.skin + "/fly_1.png",playerDirection)

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

def AnimeLootBox(player: [Object.GameObject]):

    global playerSize
    if playerSize >= 400: Constants.currentScene = "Extra_Menu"
    else:
        playerSize += 10
        print(playerSize, player.data)
        player.Resize((Constants.playerSize, Constants.playerSize))