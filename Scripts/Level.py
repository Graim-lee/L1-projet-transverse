import pygame
import Scripts.Constants as Constants
import Scripts.Physics as Physics
import Scripts.InputsManager as InputsManager
import Scripts.Object as Object

mainPooler = Object.Pooler(["Player", "Wall", "Trajectory", "Fuck"])

def Level0():
    # Pooler object from the Object.py script. See there to get a description.
    global mainPooler
    pooler = mainPooler.Copy()

    # Creating the player's character.
    playerPos = (Constants.screenDimensions[0] / 2, 500)
    playerSize = (44, 44)
    playerTexture = "Sprites/Player/idle.png"
    playerMass = 1
    playerLayer = 0
    player = Object.GameObject(playerPos, playerSize, playerTexture, playerMass, playerLayer, [2], "Level_0", True, True, True)
    pooler.AddObject(player, "Player")  # On met le GameObject player dans le pooler.

    # Creating the test floor.
    floorPos = (0, Constants.screenDimensions[1] - 200)
    floorSize = (Constants.screenDimensions[0] * 5, 100)
    floorTexture = "Sprites/floar.png"
    floorMass = 0
    floorLayer = 1
    floor = Object.GameObject(floorPos, floorSize, floorTexture, floorMass, floorLayer, [2], "Level_0")
    pooler.AddObject(floor, "Wall")  # We put the floor in the 'Wall' category as they share the same properties.

    # Creating the left wall.
    wallPos = (-600, 0)
    wallSize = (600, Constants.screenDimensions[1])
    wallTexture = "Sprites/wall.png"
    wallMass = 0
    wallLayer = 1
    wall = Object.GameObject(wallPos, wallSize, wallTexture, wallMass, wallLayer, [2], "Level_0")
    pooler.AddObject(wall, "Wall")

    platformPos = (1700, 650)
    platformSize = (300, 100)

    platformTexture = "Sprites/wall.png"
    platformMass = 0
    platformLayer = 1
    platform = Object.GameObject(platformPos, platformSize, platformTexture, platformMass, platformLayer, [2], "Level_0")
    pooler.AddObject(platform, "Wall")

    fuckPos = (Constants.screenDimensions[0] / 2 - 240, 200)
    fuckSize = (480, 160)
    fuckTexture = "Sprites/fuck.png"
    fuckMass = 0
    fuckLayer = 0
    fuck = Object.GameObject(fuckPos, fuckSize, fuckTexture, fuckMass, fuckLayer, [2], "Pause_Menu", _png=True)
    pooler.AddObject(fuck, "Fuck")

    # We link different objects to different scripts.
    InputsManager.SetPooler(pooler)
    InputsManager.SetPlayer(player)
    Physics.SetPooler(pooler)
    Physics.SetPlayer(player)

    return pooler