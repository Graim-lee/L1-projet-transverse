import pygame
import Scripts.Constants as Constants
import Scripts.Physics as Physics
import Scripts.InputsManager as InputsManager
import Scripts.Object as Object
import Scripts.ButtonFunctions as ButtonFunctions

mainPooler = Object.Pooler(["Text", "Button", "Player", "Wall", "Trajectory"])

def Level0():
    # Pooler object from the Object.py script. See there to get a description.
    global mainPooler
    pooler = mainPooler.Copy()

    # Creating the player's character.
    playerPos = (Constants.screenDimensions[0] / 2, 500)
    playerSize = (44, 44)
    playerTexture = "Sprites/Player/idle.png"
    playerMass = 1
    playerLayer = 1
    player = Object.GameObject(playerPos, playerSize, "Level_0", "Real", playerTexture, playerMass, playerLayer, [0], True, True, True)
    pooler.AddObject(player, "Player")  # On met le GameObject player dans le pooler.

    # Creating the test floor.
    floorPos = (0, Constants.screenDimensions[1] - 200)
    floorSize = (Constants.screenDimensions[0] * 5, 100)
    floorTexture = "Sprites/floar.png"
    floorMass = 0
    floorLayer = 2
    floor = Object.GameObject(floorPos, floorSize, "Level_0", "Real", floorTexture, floorMass, floorLayer, [0])
    pooler.AddObject(floor, "Wall")  # We put the floor in the 'Wall' category as they share the same properties.

    # Creating the left wall.
    wallPos = (-600, 0)
    wallSize = (600, Constants.screenDimensions[1])
    wallTexture = "Sprites/wall.png"
    wallMass = 0
    wallLayer = 2
    wall = Object.GameObject(wallPos, wallSize, "Level_0", "Real", wallTexture, wallMass, wallLayer, [0])
    pooler.AddObject(wall, "Wall")

    platformPos = (1700, 650)
    platformSize = (300, 100)

    platformTexture = "Sprites/wall.png"
    platformMass = 0
    platformLayer = 2
    platform = Object.GameObject(platformPos, platformSize, "Level_0", "Real", platformTexture, platformMass, platformLayer, [0])
    pooler.AddObject(platform, "Wall")

    pauseTitlePos = (Constants.screenDimensions[0] / 2 - 140, 200)
    pauseTitle = Object.GameObject(pauseTitlePos, (0,0), "Pause_Menu", "Text", ("Pause", True), 0, 0, [0])
    pooler.AddObject(pauseTitle, "Text")

    fuckPos = (Constants.screenDimensions[0] / 2 - 100, 600)
    fuck = Object.GameObject(fuckPos, (0,0), "Level_0", "Text", ("fuck u lol (for debug purposes)", False), 0, 0, [0])
    pooler.AddObject(fuck, "Text")

    buttonPos = (Constants.screenDimensions[0] / 2 - 100, 600)
    button = Object.GameObject(buttonPos, (0,0), "Pause_Menu", "Button", ("Quit", ButtonFunctions.QuitGame), 0, 0, [0])
    pooler.AddObject(button, "Button")

    # We link different objects to different scripts.
    InputsManager.SetPooler(pooler)
    InputsManager.SetPlayer(player)
    Physics.SetPooler(pooler)
    Physics.SetPlayer(player)

    return pooler