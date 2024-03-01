import pygame
import Scripts.Constants as Constants
import Scripts.Physics as Physics
import Scripts.InputsManager as InputsManager
import Scripts.Object as Object
import Scripts.ButtonFunctions as ButtonFunctions

initPooler = Object.Pooler(["Text", "Button", "Player", "Wall", "Trajectory"])

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
    button = Object.GameObject(buttonPos, (0,0), "Main_Menu", "Button", ("Play", ButtonFunctions.ToWorldSelection), 0, 0, [0])
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
    player = Object.GameObject((0,0), playerSize, "Level_0", "Real", playerTexture, 1, 1, [0], True, True, True)
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


""" LIST OF EVERY SCENE :

    - Main_Menu: the base scene (the one in which we are when we start the game), the main menu.
    - World_Selection: the world selection scene. Accessible after clicking on "Play" in the main menu.
    - Pause_Menu: the pause menu.
    
    - Level_0: the playtest level.

"""