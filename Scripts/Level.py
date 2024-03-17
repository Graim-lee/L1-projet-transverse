import pygame
import Scripts.Constants as Constants
import Scripts.Physics as Physics
import Scripts.InputsManager as InputsManager
import Scripts.Object as Object
import Scripts.ButtonFunctions as ButtonFunctions

initPooler = Object.Pooler()
initDictionary = {"Door": [], "Wall": [], "Text": [], "Trajectory": [], "Button": [], "Player": []}

def GetPooler() -> Object.Pooler:
    """ Returns the whole game's pooler by calling each scene's pooler individually. I checked for performance issues,
     and it seems that having that many objects at the same time in the pooler isn't bad. What matters is how many objects
     are on-screen at the same time. """
    pooler = initPooler.Copy()

    pooler.SetScene("Level_All", All())
    pooler.SetScene("Main_Menu", MainMenu())
    pooler.SetScene("World_Selection", WorldSelection())
    pooler.SetScene("Level_World_Selection", LevelWorldSelection())
    pooler.SetScene("World_1", World_1())
    pooler.SetScene("Level_World_1", LevelWorld_1())
    pooler.SetScene("Pause_Menu", PauseMenu())
    pooler.SetScene("Level_1", Level_1())
    pooler.SetScene("Level_2", Level_2())
    pooler.SetScene("Level_3", Level_3())
    pooler.SetScene("Level_4", Level_4())

    for scene in pooler.main:
        print("==========================================================================\n" + scene + "\n")
        for category in pooler.main[scene]:
            for obj in pooler.main[scene][category]:
                print(category + " : " + str(obj))

    return pooler

def PauseMenu():
    """ Adds the Pause Menu pooler to the main pooler. """
    result = CopyDict(initDictionary)

    # Title ("Pause").
    objectPos = (Constants.screenDimensions[0] / 2, 270)
    gameObject = Object.GameObject(objectPos, (0, 0), "Pause_Menu", "Text", ("Pause", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # ESC to restart the game
    objectPos = (Constants.screenDimensions[0] / 2, 400)
    gameObject = Object.GameObject(objectPos, (0, 0), "Pause_Menu", "Text", ("Press ESC to get back to the game", False), 0, 0, [0])
    result["Text"].append(gameObject)

    # "Back to menu" button.
    objectPos = (Constants.screenDimensions[0] / 2, 600)
    gameObject = Object.GameObject(objectPos, (200, 80), "Pause_Menu", "Button", ("Back to menu", ButtonFunctions.ToMainMenu), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Quit game" button.
    objectPos = (Constants.screenDimensions[0] / 2, 770)
    gameObject = Object.GameObject(objectPos, (160, 70), "Pause_Menu", "Button", ("Quit", ButtonFunctions.QuitGame), 0, 0, [0])
    result["Button"].append(gameObject)

    return result

def MainMenu():
    """ Adds the Main Menu pooler to the main pooler. """
    global initDictionary
    result = CopyDict(initDictionary)

    # Title of the game.
    objectPos = (Constants.screenDimensions[0] / 2, 270)
    gameObject = Object.GameObject(objectPos, (0,0), "Main_Menu", "Text", ("Penguin Run", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # "Play game" button.
    objectPos = (Constants.screenDimensions[0] / 2, 500)
    gameObject = Object.GameObject(objectPos, (160, 70), "Main_Menu", "Button", ("Play", ButtonFunctions.ToWorldSelection), 0, 0, [0])
    result["Button"].append(gameObject)

    # "World selection test menu" button.
    objectPos = (Constants.screenDimensions[0] / 2, 625)
    gameObject = Object.GameObject(objectPos, (340, 70), "Main_Menu", "Button", ("World select", ButtonFunctions.ToLevel_WorldSelection), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Quit game" button.
    objectPos = (Constants.screenDimensions[0] / 2, 770)
    gameObject = Object.GameObject(objectPos, (160, 70), "Main_Menu", "Button", ("Quit", ButtonFunctions.QuitGame), 0, 0, [0])
    result["Button"].append(gameObject)

    # Penguin sprite on the left of the screen
    objectPos = (Constants.screenDimensions[0] / 2 - 500, 450)
    gameObject = Object.GameObject(objectPos, (200,200), "Main_Menu","Real", "Sprites/Player/idle.png", 0, 0, [0],True,True,False)
    result["Text"].append(gameObject)

    # Penguin sprite on the right of the screen
    objectPos = (Constants.screenDimensions[0] / 2 + 300, 450)
    gameObject = Object.GameObject(objectPos, (200,200), "Main_Menu","Real", "Sprites/Player/idle.png", 0, 0, [0],True,True,False)
    result["Text"].append(gameObject)

    return result

def LevelWorldSelection():
    """ Adds the World Selection lobby to the main pooler. """
    global initDictionary
    result = CopyDict(initDictionary)

    wallTexture = "Sprites/wall.png"
    doorTexture = "Sprites/door.png"

    # World 1 door.
    objectPos = (1450, Constants.screenDimensions[1] - 650)
    blockSize = (100, 200)
    gameObject = Object.GameObject(objectPos, blockSize, "Level_World_Selection", "Door", (doorTexture, ButtonFunctions.ToLevel_World1), 0, 3, [0])
    result["Door"].append(gameObject)

    # World 1 door "WORLD 1" text.
    objectPos = (1500, Constants.screenDimensions[1] - 700)
    gameObject = Object.GameObject(objectPos, (0, 0), "Level_World_Selection", "Text", ("WORLD 1", False), 0, 0, [0])
    result["Text"].append(gameObject)

    # Floor.
    objectPos = (0, Constants.screenDimensions[1] - 500)
    floorSize = (Constants.screenDimensions[0] * 5, 800)
    gameObject = Object.GameObject(objectPos, floorSize, "Level_World_Selection", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    return result

def LevelWorld_1():
    """ Adds the World 1 lobby pooler to the main pooler. """
    global initDictionary
    result = CopyDict(initDictionary)

    wallTexture = "Sprites/wall.png"
    doorTexture = "Sprites/door.png"

    # Floor.
    objectPos = (0, Constants.screenDimensions[1] - 500)
    floorSize = (Constants.screenDimensions[0] * 5, 800)
    gameObject = Object.GameObject(objectPos, floorSize, "Level_World_1", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    return result

def WorldSelection():
    """ Adds the World Selection pooler to the main pooler. """
    global initDictionary
    result = CopyDict(initDictionary)

    # Title "World selection".
    objectPos = (Constants.screenDimensions[0] / 2, 240)
    gameObject = Object.GameObject(objectPos, (0,0), "World_Selection", "Text", ("World selection", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # "World 1" button.
    objectPos = (1 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2 - 100)
    gameObject = Object.GameObject(objectPos, (200, 200), "World_Selection", "WorldButton", ("WORLD 1", ButtonFunctions.ToWorld_1, "Sprites/Worlds/world1.png"), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Quit Game" button.
    objectPos = (Constants.screenDimensions[0] / 2, 900)
    gameObject = Object.GameObject(objectPos, (160, 70), "World_Selection", "Button", ("Quit", ButtonFunctions.QuitGame), 0, 0, [0])
    result["Button"].append(gameObject)

    return result

def World_1():
    """ Adds the World 1 level selection menu pooler to the main pooler. """
    global initDictionary
    result = CopyDict(initDictionary)

    # Title "World 1".
    objectPos = (Constants.screenDimensions[0] / 2, 240)
    gameObject = Object.GameObject(objectPos, (0,0), "World_1", "Text", ("World 1", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # "Level 1" button.
    objectPos = (1 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    gameObject = Object.GameObject(objectPos, (200, 160), "World_1", "Button", ("Level 1", ButtonFunctions.ToLevel_World1), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Level 2" button.
    objectPos = (2 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    gameObject = Object.GameObject(objectPos, (200, 160), "World_1", "Button", ("Level 2", ButtonFunctions.ToLevel_2), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Level 3" button.
    objectPos = (3 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    gameObject = Object.GameObject(objectPos, (200, 160), "World_1", "Button", ("Level 3", ButtonFunctions.ToLevel_3), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Level 4" Button.
    objectPos = (4 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    gameObject = Object.GameObject(objectPos, (200, 160), "World_1", "Button", ("Level 4", ButtonFunctions.ToLevel_4), 0, 0, [0])
    result["Button"].append(gameObject)

    return result

def All():
    """ Adds the objects that are always loaded to the pooler. """
    global initDictionary
    result = CopyDict(initDictionary)

    # Player.
    playerSize = (44, 44)
    playerTexture = "Sprites/Player/idle.png"
    gameObject = Object.GameObject((0,0), playerSize, "Level_All", "Real", playerTexture, 1, 1, [0, 3], True, True, True)
    result["Player"].append(gameObject)

    # Trajectory dots.
    for i in range(5):
        gameObject = Object.GameObject((0, 0), (10 - i, 10 - i), "Level_All", "Real", "Sprites/dot.png", 0, 0, [0, 1, 2, 3])
        result["Trajectory"].append(gameObject)

    return result

def Level_1():
    """ Adds the Level_0 pooler (= the playtest level) to the main pooler. """
    global initDictionary
    result = CopyDict(initDictionary)

    wallTexture = "Sprites/wall.png"

    # Floor.
    objectPos = (0, Constants.screenDimensions[1] - 200)
    floorSize = (Constants.screenDimensions[0] * 5, 100)
    gameObject = Object.GameObject(objectPos, floorSize, "Level_1", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left wall.
    objectPos = (-600, 0)
    wallSize = (600, Constants.screenDimensions[1])
    gameObject = Object.GameObject(objectPos, wallSize, "Level_1", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Platform.
    objectPos = (1700, 650)
    platformSize = (300, 100)
    gameObject = Object.GameObject(objectPos, platformSize, "Level_1", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # "Fuck u" debug text.
    objectPos = (Constants.screenDimensions[0] / 2 - 100, 600)
    gameObject = Object.GameObject(objectPos, (0,0), "Level_1", "Text", ("fuck u lol (for debug purposes)", False), 0, 0, [0])
    result["Text"].append(gameObject)

    # Platform 2.
    objectPos = (2200, 650)
    platformSize = (300, 100)
    gameObject = Object.GameObject(objectPos, platformSize, "Level_1", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Platform 3.
    objectPos = (2200, 400)
    platformSize = (300, 100)
    gameObject = Object.GameObject(objectPos, platformSize, "Level_1", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    return result

def Level_2():
    """ Adds the Level_0 pooler (= the playtest level) to the main pooler. """
    global initDictionary
    result = CopyDict(initDictionary)

    wallTexture = "Sprites/wall.png"

    # Floor.
    objectPos = (0, Constants.screenDimensions[1] - 200)
    floorSize = (Constants.screenDimensions[0] * 5, 100)
    gameObject = Object.GameObject(objectPos, floorSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left wall.
    objectPos = (-600, 0)
    wallSize = (600, Constants.screenDimensions[1])
    gameObject = Object.GameObject(objectPos, wallSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # "Fuck u" debug text.
    objectPos = (Constants.screenDimensions[0] / 2 - 100, 600)
    gameObject = Object.GameObject(objectPos, (0,0), "Level_2", "Text", ("fuck u lol (for debug purposes)", False), 0, 0, [0])
    result["Wall"].append(gameObject)

    # Platform 1.
    objectPos = (1700, 650)
    platformSize = (300, 100)
    gameObject = Object.GameObject(objectPos, platformSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Platform 2.
    objectPos = (2200, 650)
    platform2Size = (300, 100)
    gameObject = Object.GameObject(objectPos, platform2Size, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Platform 3.
    objectPos = (2200, 400)
    platform3Size = (300, 100)
    gameObject = Object.GameObject(objectPos, platform3Size, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    return result

def Level_3():
    """ Adds the Level_0 pooler (= the playtest level) to the main pooler. """
    global initDictionary
    result = CopyDict(initDictionary)

    wallTexture = "Sprites/wall.png"

    # Left stair n°2.
    objectPos = (500, 680)
    wallSize = (200, 200)
    gameObject = Object.GameObject(objectPos, wallSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left stair n°1.
    objectPos = (500, 780)
    wallSize = (300, 200)
    gameObject = Object.GameObject(objectPos, wallSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Right platform.
    objectPos = (2000, 500)
    wallSize = (700, 500)
    gameObject = Object.GameObject(objectPos, wallSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Walljump platform 1.
    objectPos = (2550, 300)
    wallSize = (100, 50)
    gameObject = Object.GameObject(objectPos, wallSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Walljump platform 2.
    objectPos = (2200, 100)
    wallSize = (100, 50)
    gameObject = Object.GameObject(objectPos, wallSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Walljump platform 3.
    objectPos = (2550, -50)
    wallSize = (100, 50)
    gameObject = Object.GameObject(objectPos, wallSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Upper section block before big jump.
    objectPos = (1000, -500)
    wallSize = (200, 400)
    gameObject = Object.GameObject(objectPos, wallSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Upper section first stair.
    objectPos = (1800, -300)
    wallSize = (300, 200)
    gameObject = Object.GameObject(objectPos, wallSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Upper section second stair.
    objectPos = (1700, -400)
    wallSize = (200, 300)
    gameObject = Object.GameObject(objectPos, wallSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Upper section floor.
    objectPos = (1000, -200)
    wallSize = (1250, 100)
    gameObject = Object.GameObject(objectPos, wallSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left wall for walljump.
    objectPos = (2200, -200)
    wallSize = (50, 500)
    gameObject = Object.GameObject(objectPos, wallSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Right border.
    objectPos = (2600, -2000)
    wallSize = (500, 4000)
    gameObject = Object.GameObject(objectPos, wallSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Floor.
    objectPos = (0, Constants.screenDimensions[1] - 200)
    floorSize = (Constants.screenDimensions[0] * 5, 800)
    gameObject = Object.GameObject(objectPos, floorSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left platform.
    objectPos = (-100, 600)
    wallSize = (700, 800)
    gameObject = Object.GameObject(objectPos, wallSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Jump
    objectPos = (-100, -500)
    wallSize = (600, 400)
    gameObject = Object.GameObject(objectPos, wallSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left border.
    objectPos = (-700, -2000)
    wallSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, wallSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Parkour platform 1.
    objectPos = (900, 550)
    platformSize = (200, 50)
    gameObject = Object.GameObject(objectPos, platformSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Parkour platform 2.
    objectPos = (1250, 550)
    platformSize = (200, 50)
    gameObject = Object.GameObject(objectPos, platformSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Parkour platform 3.
    objectPos = (1650, 550)
    platformSize = (200, 50)
    gameObject = Object.GameObject(objectPos, platformSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    return result

def Level_4():
    global initDictionary
    result = CopyDict(initDictionary)

    objectPos = (544, 844)
    platformSize = (1000, 1000)
    gameObject = Object.GameObject(objectPos, platformSize, "Level_4", "Real", "Sprites/wall.png", 0, 2, [0])
    result["Wall"].append(gameObject)

    return result





def CopyDict(dictionary: {}) -> {}:
    """ Returns an UNLINKED copy of the given dictionary, meaning changing the value of the new dictionary (the copy)
    won't affect the initial dictionary.
        Args:
            - dictionary ({}): the dictionary to copy.
        Returns:
            - ({}): a copy of the dictionary.
    """
    result = {}
    for category in dictionary:
        result[category] = list(dictionary[category])
    return result

""" LIST OF EVERY SCENE :

    - Main_Menu: the base scene (the one in which we are when we start the game), the main menu.
    - World_Selection: the world selection scene. Accessible after clicking on "Play" in the main menu.
    - World_1: the level selection menu of world 1.
    - Pause_Menu: the pause menu.
    
    - Level_0: the playtest level.

"""