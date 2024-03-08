import pygame
import Scripts.Constants as Constants
import Scripts.Physics as Physics
import Scripts.InputsManager as InputsManager
import Scripts.Object as Object
import Scripts.ButtonFunctions as ButtonFunctions

initPooler = Object.Pooler(["Wall", "Door", "Player", "Trajectory", "Button", "Text"])

def BasePooler() -> Object.Pooler:
    """ Returns the whole game's pooler by calling each scene's pooler individually. I checked for performance issues,
     and it seems that having that many objects at the same time in the pooler isn't bad. What matters is how many objects
     are on-screen at the same time. """
    pooler = initPooler.Copy()

    Player(pooler)

    MainMenu(pooler)
    WorldSelection(pooler)
    LevelWorldSelection(pooler)
    World_1(pooler)

    PauseMenu(pooler)

    Level_1(pooler)
    Level_2(pooler)
    Level_3(pooler)

    return pooler

def PauseMenu(pooler: Object.Pooler):
    """ Adds the Pause Menu pooler to the main pooler. """
    # Title ("Pause").
    pauseTitlePos = (Constants.screenDimensions[0] / 2, 270)
    pauseTitle = Object.GameObject(pauseTitlePos, (0, 0), "Pause_Menu", "Text", ("Pause", True), 0, 0, [0])
    pooler.AddObject(pauseTitle, "Text")

    # ESC to restart the game
    restartPos = (Constants.screenDimensions[0] / 2, 400)
    restartT = Object.GameObject(restartPos, (0, 0), "Pause_Menu", "Text", ("Press ESC to get back to the game", False), 0, 0, [0])
    pooler.AddObject(restartT, "Text")

    # "Back to menu" button.
    buttonPos = (Constants.screenDimensions[0] / 2, 600)
    button = Object.GameObject(buttonPos, (200, 80), "Pause_Menu", "Button", ("Back to menu", ButtonFunctions.ToMainMenu), 0, 0, [0])
    pooler.AddObject(button, "Button")

    # "Quit game" button.
    buttonPos = (Constants.screenDimensions[0] / 2, 770)
    button = Object.GameObject(buttonPos, (160, 70), "Pause_Menu", "Button", ("Quit", ButtonFunctions.QuitGame), 0, 0, [0])
    pooler.AddObject(button, "Button")

def MainMenu(pooler: Object.Pooler):
    """ Adds the Main Menu pooler to the main pooler. """
    # Title of the game.
    mainTitlePos = (Constants.screenDimensions[0] / 2, 270)
    mainTitle = Object.GameObject(mainTitlePos, (0,0), "Main_Menu", "Text", ("Penguin Run", True), 0, 0, [0])
    pooler.AddObject(mainTitle, "Text")

    # "Play game" button.
    gameButtonPos = (Constants.screenDimensions[0] / 2, 500)
    gameButton = Object.GameObject(gameButtonPos, (160, 70), "Main_Menu", "Button", ("Play", ButtonFunctions.ToWorldSelection), 0, 0, [0])
    pooler.AddObject(gameButton, "Button")

    # "World selection test menu" button.
    gameButtonPos = (Constants.screenDimensions[0] / 2, 625)
    gameButton = Object.GameObject(gameButtonPos, (340, 70), "Main_Menu", "Button", ("World select", ButtonFunctions.ToLevel_WorldSelection), 0, 0, [0])
    pooler.AddObject(gameButton, "Button")

    # "Quit game" button.
    buttonPos = (Constants.screenDimensions[0] / 2, 770)
    button = Object.GameObject(buttonPos, (160, 70), "Main_Menu", "Button", ("Quit", ButtonFunctions.QuitGame), 0, 0, [0])
    pooler.AddObject(button, "Button")

    # Penguin sprite on the left of the screen
    penguinPos = (Constants.screenDimensions[0] / 2 - 500, 450)
    playerTexture = "Sprites/PlayerMove/player.png"
    image = Object.GameObject(penguinPos, (200,200), "Main_Menu","Real",playerTexture,0,0,[0],True,True,False)
    pooler.AddObject(image,"Player")

    # Penguin sprite on the right of the screen
    penguinPos = (Constants.screenDimensions[0] / 2 + 300, 450)
    playerTexture = "Sprites/PlayerMove/player_reverse.png"
    image = Object.GameObject(penguinPos, (200,200), "Main_Menu","Real",playerTexture,0,0,[0],True,True,False)
    pooler.AddObject(image,"Player")

def LevelWorldSelection(pooler: Object.Pooler):
    """ Adds the World Selection lobby to the main pooler. """
    wallTexture = "Sprites/wall.png"

    # Right stair 2.
    blockPos = (1400, Constants.screenDimensions[1] - 600)
    blockSize = (200, 100)
    block = Object.GameObject(blockPos, blockSize, "Level_World_Selection", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(block, "Wall")

    # Right stair 1.
    blockPos = (1300, Constants.screenDimensions[1] - 550)
    blockSize = (300, 100)
    block = Object.GameObject(blockPos, blockSize, "Level_World_Selection", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(block, "Wall")

    # Right platform.
    blockPos = (1500, Constants.screenDimensions[1] - 650)
    blockSize = (500, 200)
    block = Object.GameObject(blockPos, blockSize, "Level_World_Selection", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(block, "Wall")

    # Floor.
    floorPos = (0, Constants.screenDimensions[1] - 500)
    floorSize = (Constants.screenDimensions[0] * 5, 800)
    floor = Object.GameObject(floorPos, floorSize, "Level_World_Selection", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(floor, "Wall")

def WorldSelection(pooler: Object.Pooler):
    """ Adds the World Selection pooler to the main pooler. """
    # Title "World selection".
    worldTitlePos = (Constants.screenDimensions[0] / 2, 240)
    worldTitle = Object.GameObject(worldTitlePos, (0,0), "World_Selection", "Text", ("World selection", True), 0, 0, [0])
    pooler.AddObject(worldTitle, "Text")

    # "World 1" button.
    buttonPos = (1 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2 - 100)
    button = Object.GameObject(buttonPos, (200, 200), "World_Selection", "WorldButton", ("WORLD 1", ButtonFunctions.ToWorld_1, "Sprites/Worlds/world1.png"), 0, 0, [0])
    pooler.AddObject(button, "Button")

    # "Quit Game" button.
    buttonPosQuit = (Constants.screenDimensions[0] / 2, 900)
    buttonQuit = Object.GameObject(buttonPosQuit, (160, 70), "World_Selection", "Button", ("Quit", ButtonFunctions.QuitGame), 0, 0, [0])
    pooler.AddObject(buttonQuit, "Button")

def World_1(pooler: Object.Pooler):
    """ Adds the World 1 level selection menu pooler to the main pooler. """
    # Title "World 1".
    worldTitlePos = (Constants.screenDimensions[0] / 2, 240)
    worldTitle = Object.GameObject(worldTitlePos, (0,0), "World_1", "Text", ("World 1", True), 0, 0, [0])
    pooler.AddObject(worldTitle, "Text")

    # "Level 1" button.
    buttonPos0 = (1 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    button0 = Object.GameObject(buttonPos0, (200, 160), "World_1", "Button", ("Level 1", ButtonFunctions.ToLevel_0), 0, 0, [0])
    pooler.AddObject(button0, "Button")

    # "Level 2" button.
    buttonPos1 = (2 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    button1 = Object.GameObject(buttonPos1, (200, 160), "World_1", "Button", ("Level 2", ButtonFunctions.ToLevel_1), 0, 0, [0])
    pooler.AddObject(button1, "Button")

    # "Level 3" button.
    buttonPos2 = (3 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    button2 = Object.GameObject(buttonPos2, (200, 160), "World_1", "Button", ("Level 3", ButtonFunctions.ToLevel_2), 0, 0, [0])
    pooler.AddObject(button2, "Button")

    # "Level 4" Button.
    buttonPos3 = (4 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    button3 = Object.GameObject(buttonPos3, (200, 160), "World_1", "Button", ("Level 4", ButtonFunctions.ToLevel_2), 0, 0, [0])
    pooler.AddObject(button3, "Button")

def Player(pooler: Object.Pooler):
    """ Adds the player to the main pooler (necessary for most scripts to work). """
    playerSize = (44, 44)
    playerTexture = "Sprites/Player/idle.png"
    player = Object.GameObject((0,0), playerSize, "Level_All", "Real", playerTexture, 1, 1, [0, 3], True, True, True)
    pooler.AddObject(player, "Player")

def Level_1(pooler: Object.Pooler):
    """ Adds the Level_0 pooler (= the playtest level) to the main pooler. """
    wallTexture = "Sprites/wall.png"

    # Floor.
    floorPos = (0, Constants.screenDimensions[1] - 200)
    floorSize = (Constants.screenDimensions[0] * 5, 100)
    floor = Object.GameObject(floorPos, floorSize, "Level_0", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(floor, "Wall")  # We put the floor in the 'Wall' category as they share the same properties.

    # Left wall.
    wallPos = (-600, 0)
    wallSize = (600, Constants.screenDimensions[1])
    wall = Object.GameObject(wallPos, wallSize, "Level_0", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Platform.
    platformPos = (1700, 650)
    platformSize = (300, 100)
    platform = Object.GameObject(platformPos, platformSize, "Level_0", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(platform, "Wall")

    # "Fuck u" debug text.
    fuckPos = (Constants.screenDimensions[0] / 2 - 100, 600)
    fuck = Object.GameObject(fuckPos, (0,0), "Level_0", "Text", ("fuck u lol (for debug purposes)", False), 0, 0, [0])
    pooler.AddObject(fuck, "Text")

    # platform 2.
    platformPos = (2200, 650)
    platformSize = (300, 100)
    platform = Object.GameObject(platformPos, platformSize, "Level_0", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(platform, "Wall")

    # platform 3.
    platformPos = (2200, 400)
    platformSize = (300, 100)
    platform = Object.GameObject(platformPos, platformSize, "Level_0", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(platform, "Wall")

def Level_2(pooler: Object.Pooler):
    """ Adds the Level_0 pooler (= the playtest level) to the main pooler. """
    wallTexture = "Sprites/wall.png"

    # Floor.
    floorPos = (0, Constants.screenDimensions[1] - 200)
    floorSize = (Constants.screenDimensions[0] * 5, 100)
    floor = Object.GameObject(floorPos, floorSize, "Level_1", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(floor, "Wall")  # We put the floor in the 'Wall' category as they share the same properties.

    # Left wall.
    wallPos = (-600, 0)
    wallSize = (600, Constants.screenDimensions[1])
    wall = Object.GameObject(wallPos, wallSize, "Level_1", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # "Fuck u" debug text.
    fuckPos = (Constants.screenDimensions[0] / 2 - 100, 600)
    fuck = Object.GameObject(fuckPos, (0,0), "Level_1", "Text", ("fuck u lol (for debug purposes)", False), 0, 0, [0])
    pooler.AddObject(fuck, "Text")

    # Platform 1.
    platformPos = (1700, 650)
    platformSize = (300, 100)
    platform = Object.GameObject(platformPos, platformSize, "Level_1", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(platform, "Wall")

    # Platform 2.
    platform2Pos = (2200, 650)
    platform2Size = (300, 100)
    platform2 = Object.GameObject(platform2Pos, platform2Size, "Level_1", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(platform2, "Wall")

    # Platform 3.
    platform3Pos = (2200, 400)
    platform3Size = (300, 100)
    platform3 = Object.GameObject(platform3Pos, platform3Size, "Level_1", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(platform3, "Wall")


def Level_3(pooler: Object.Pooler):
    """ Adds the Level_0 pooler (= the playtest level) to the main pooler. """
    wallTexture = "Sprites/wall.png"

    # Left wall small.
    wallPos = (500, 680)
    wallSize = (200, 200)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Left wall small.
    wallPos = (500, 780)
    wallSize = (300, 200)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Right platform.
    wallPos = (2000, 500)
    wallSize = (700, 500)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Walljump platform 1
    wallPos = (2550, 300)
    wallSize = (100, 50)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Walljump platform 2
    wallPos = (2200, 100)
    wallSize = (100, 50)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Walljump platform 3
    wallPos = (2550, -50)
    wallSize = (100, 50)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Upper section block before big jump.
    wallPos = (1000, -500)
    wallSize = (200, 400)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Upper section first stair.
    wallPos = (1800, -300)
    wallSize = (300, 200)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Upper section second stair.
    wallPos = (1700, -400)
    wallSize = (200, 300)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Upper section floor.
    wallPos = (1000, -200)
    wallSize = (1250, 100)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Left wall for walljump.
    wallPos = (2200, -200)
    wallSize = (50, 500)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Right border.
    wallPos = (2600, -2000)
    wallSize = (500, 4000)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Floor.
    floorPos = (0, Constants.screenDimensions[1] - 200)
    floorSize = (Constants.screenDimensions[0] * 5, 800)
    floor = Object.GameObject(floorPos, floorSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(floor, "Wall")

    # Left platform.
    wallPos = (-100, 600)
    wallSize = (700, 800)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Jump
    wallPos = (-100, -500)
    wallSize = (600, 400)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Left border.
    wallPos = (-700, -2000)
    wallSize = (1000, 4000)
    wall = Object.GameObject(wallPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(wall, "Wall")

    # Parkour platform 1.
    platformPos = (900, 550)
    platformSize = (200, 50)
    platform = Object.GameObject(platformPos, platformSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(platform, "Wall")

    # Parkour platform 2.
    platformPos = (1250, 550)
    platformSize = (200, 50)
    platform = Object.GameObject(platformPos, platformSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(platform, "Wall")

    # Parkour platform 3.
    platformPos = (1650, 550)
    platformSize = (200, 50)
    platform = Object.GameObject(platformPos, platformSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    pooler.AddObject(platform, "Wall")


""" LIST OF EVERY SCENE :

    - Main_Menu: the base scene (the one in which we are when we start the game), the main menu.
    - World_Selection: the world selection scene. Accessible after clicking on "Play" in the main menu.
    - World_1: the level selection menu of world 1.
    - Pause_Menu: the pause menu.
    
    - Level_0: the playtest level.

"""