import pygame
import Scripts.Constants as Constants
import Scripts.Physics as Physics
import Scripts.InputsManager as InputsManager
import Scripts.Object as Object
import Scripts.ButtonFunctions as ButtonFunctions

initPooler = Object.Pooler(["Text", "Button", "Player", "Wall", "Trajectory","Door"])

def BasePooler() -> Object.Pooler:
    """ Returns the whole game's pooler by calling each scene's pooler individually. I checked for performance issues,
     and it seems that having that many objects at the same time in the pooler isn't bad. What matters is how many objects
     are on-screen at the same time. """
    pooler = initPooler.Copy()

    Player(pooler)

    PauseMenu(pooler)
    MainMenu(pooler)
    WorldSelection(pooler)

    Level_0(pooler)
    Level_2(pooler)

    return pooler

def PauseMenu(pooler: Object.Pooler):
    """ Adds the Pause Menu pooler to the main pooler. """
    # Title ("Pause").
    pauseTitlePos = (Constants.screenDimensions[0] / 2 - 140, 200)
    pauseTitle = Object.GameObject(pauseTitlePos, (0,0), "Pause_Menu", "Text", ("Pause", True), 0, 0, [0])
    pooler.AddObject(pauseTitle, "Text")

    # "Quit game" button.
    buttonPos = (Constants.screenDimensions[0] / 2 - 100, 600)
    button = Object.GameObject(buttonPos, (0,0), "Pause_Menu", "Button", ("Quit", ButtonFunctions.QuitGame), 0, 0, [0])
    pooler.AddObject(button, "Button")

def MainMenu(pooler: Object.Pooler):
    """ Adds the Main Menu pooler to the main pooler. """
    # Title "Main menu" (placeholder for the true name of the game).
    mainTitlePos = (Constants.screenDimensions[0] / 2 - 140, 200)
    mainTitle = Object.GameObject(mainTitlePos, (0,0), "Main_Menu", "Text", ("Main menu", True), 0, 0, [0])
    pooler.AddObject(mainTitle, "Text")

    # "Play" button.
    buttonPos = (Constants.screenDimensions[0] / 2 - 100, 700)
    button = Object.GameObject(buttonPos, (0,0), "Main_Menu", "Button", ("Play", ButtonFunctions.ToLevel_2), 0, 0, [0])
    pooler.AddObject(button, "Button")

    # "Quit game" button.
    buttonPos = (Constants.screenDimensions[0] / 2 - 100, 820)
    button = Object.GameObject(buttonPos, (0,0), "Main_Menu", "Button", ("Quit", ButtonFunctions.QuitGame), 0, 0, [0])
    pooler.AddObject(button, "Button")

    # Debug text.
    mainTitle = Object.GameObject((0,0), (0,0), "Main_Menu", "Text", ("OOOOOOOO", True), 0, 0, [0])
    pooler.AddObject(mainTitle, "Text")

def WorldSelection(pooler: Object.Pooler):
    """ Adds the World Selection pooler to the main pooler. """
    # Title "World selection".
    worldTitlePos = (Constants.screenDimensions[0] / 2 - 140, 200)
    worldTitle = Object.GameObject(worldTitlePos, (0,0), "World_Selection", "Text", ("World selection", True), 0, 0, [0])
    pooler.AddObject(worldTitle, "Text")

def Player(pooler: Object.Pooler):
    """ Adds the player to the main pooler (necessary for most scripts to work). """
    playerSize = (44, 44)
    playerTexture = "Sprites/Player/idle.png"
    player = Object.GameObject((0,0), playerSize, "Level_All", "Real", playerTexture, 1, 1, [0, 3], True, True, True)
    pooler.AddObject(player, "Player")

def Level_0(pooler: Object.Pooler):
    """ Adds the Level_0 pooler (= the playtest level) to the main pooler. """
    # Floor.
    floorPos = (0, Constants.screenDimensions[1] - 200)
    floorSize = (Constants.screenDimensions[0] * 5, 100)
    floorTexture = "Sprites/floor.png"
    floor = Object.GameObject(floorPos, floorSize, "Level_0", "Real", floorTexture, 0, 2, [0])
    pooler.AddObject(floor, "Wall")  # We put the floor in the 'Wall' category as they share the same properties.

    # Left wall.
    wallPos = (-600, 0)
    wallSize = (600, Constants.screenDimensions[1])
    wallTexture = "Sprites/wall.png"
    wall = Object.GameObject(wallPos, wallSize, "Level_0", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Platform.
    platformPos = (1700, 650)
    platformSize = (300, 100)
    platformTexture = "Sprites/wall.png"
    platform = Object.GameObject(platformPos, platformSize, "Level_0", "Real", platformTexture, 0, 2, [0])
    pooler.AddObject(platform, "Wall")

    # "Fuck u" debug text.
    fuckPos = (Constants.screenDimensions[0] / 2 - 100, 600)
    fuck = Object.GameObject(fuckPos, (0,0), "Level_0", "Text", ("fuck u lol (for debug purposes)", False), 0, 0, [0])
    pooler.AddObject(fuck, "Text")

    # platform 2.
    platform2Pos = (2200, 650)
    platform2Size = (300, 100)
    platform2Texture = "Sprites/wall.png"
    platform2 = Object.GameObject(platform2Pos, platform2Size, "Level_0", "Real", platform2Texture, 0, 2, [0])
    pooler.AddObject(platform2, "Wall")

    # platform 3.
    platform3Pos = (2200, 400)
    platform3Size = (300, 100)
    platform3Texture = "Sprites/wall.png"
    platform3 = Object.GameObject(platform3Pos, platform3Size, "Level_0", "Real", platform3Texture, 0, 2, [0])
    pooler.AddObject(platform3, "Wall")

def Level_2(pooler: Object.Pooler):
    """ Adds the Level_0 pooler (= the playtest level) to the main pooler. """

    """
    Ground
    """
    wallTexture = "Sprites/wall.png"

    # Floor.
    floorPos = (0, Constants.screenDimensions[1] - 200)
    floorSize = (Constants.screenDimensions[0] * 5, 100)
    floor = Object.GameObject(floorPos, floorSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(floor, "Wall")  # We put the floor in the 'Wall' category as they share the same properties.

    # Left wall border.
    wallPos = (-600, -1000)
    wallSize = (600, 2500)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # left wall small.
    wallPos = (0, 600)
    wallSize = (600, Constants.screenDimensions[1])
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # left wall small small.
    wallPos = (500, 700)
    wallSize = (200, 100)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Left wall small  small small.
    wallPos = (600, 800)
    wallSize = (200, 100)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Platform 1.
    platformPos = (900, 550)
    platformSize = (200, 50)
    platform = Object.GameObject(platformPos, platformSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(platform, "Wall")

    # Platform 2.
    platformPos = (1250, 550)
    platformSize = (200, 50)
    platform = Object.GameObject(platformPos, platformSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(platform, "Wall")

    # Platform 3.
    platformPos = (1650, 550)
    platformSize = (200, 50)
    platform = Object.GameObject(platformPos, platformSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(platform, "Wall")

    # Left
    wallPos = (2000, 500)
    wallSize = (600, 500)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    """
    Transition
    """
    # Left Border
    wallPos = (2600, -1000)
    wallSize = (500, 2000)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Left walljump
    wallPos = (2200, -200)
    wallSize = (50, 500)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    #platform 1
    wallPos = (2550, 300)
    wallSize = (50, 50)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # platform 2
    wallPos = (2250, 100)
    wallSize = (50, 50)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # platform 3
    wallPos = (2550, -50)
    wallSize = (50, 50)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    """
    Upper section
    """
    # Floor
    wallPos = (1000, -200)
    wallSize = (1200, 100)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Block big
    wallPos = (1000, -500)
    wallSize = (200, 300)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Block little
    wallPos = (1700, -400)
    wallSize = (200, 300)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Block little little
    wallPos = (1900, -300)
    wallSize = (200, 200)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Jump
    wallPos = (300, -500)
    wallSize = (200, 400)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Floor
    wallPos = (-400, -600)
    wallSize = (700, 500)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # The end ?
    #wallPos = (-400, -600)
    wallPos = ( 1400, 800)
    wallSize = (75, 80)
    wallTexture = "Sprites/door.png"
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [2])
    pooler.AddObject(wall, "Wall")

    """
    top
    """
    wallPos = (-1000, -1000)
    wallSize = (4000, 500)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Door")


""" LIST OF EVERY SCENE :

    - Main_Menu: the base scene (the one in which we are when we start the game), the main menu.
    - World_Selection: the world selection scene. Accessible after clicking on "Play" in the main menu.
    - Pause_Menu: the pause menu.
    
    - Level_0: the playtest level.

"""