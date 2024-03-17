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

    return pooler

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
        gameObject.active = False
        result["Trajectory"].append(gameObject)

    return result

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
    objectPos = (490, -70)
    objectSize = (100, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_World_Selection", "Door", (doorTexture, ButtonFunctions.ToLevel_World1), 0, 3, [0])
    result["Door"].append(gameObject)

    # World 1 door "WORLD 1" text.
    objectPos = (540, -120)
    gameObject = Object.GameObject(objectPos, (0, 0), "Level_World_Selection", "Text", ("WORLD 1", False), 0, 0, [0])
    result["Text"].append(gameObject)

    # Floor.
    objectPos = (-960, 80)
    objectSize = (Constants.screenDimensions[0] * 5, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_World_Selection", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    return result

def LevelWorld_1():
    """ Adds the World 1 lobby pooler to the main pooler. """
    global initDictionary
    result = CopyDict(initDictionary)

    wallTexture = "Sprites/wall.png"
    doorTexture = "Sprites/door.png"

    # Floor.
    objectPos = (-960, 80)
    objectSize = (1000, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_World_1", "Real", wallTexture, 0, 2, [0])
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
    gameObject = Object.GameObject(objectPos, (200, 160), "World_1", "Button", ("Level 1", ButtonFunctions.ToLevel_1), 0, 0, [0])
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

def Level_1():
    """ Adds the Level_0 pooler (= the playtest level) to the main pooler. """
    global initDictionary
    result = CopyDict(initDictionary)

    wallTexture = "Sprites/wall.png"

    # Right border.
    objectPos = (1660, -2700)
    objectSize = (500, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_1", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Floor.
    objectPos = (-940, 180)
    objectSize = (Constants.screenDimensions[0] * 5, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_1", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left border.
    objectPos = (-1200, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_1", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    return result

def Level_2():
    """ Adds the Level_0 pooler (= the playtest level) to the main pooler. """
    global initDictionary
    result = CopyDict(initDictionary)

    wallTexture = "Sprites/wall.png"

    # Left stair n°2.
    objectPos = (-775, -20)
    objectSize = (200, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left stair n°1.
    objectPos = (-775, 80)
    objectSize = (300, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Right platform.
    objectPos = (725, -200)
    objectSize = (700, 500)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Walljump platform 1.
    objectPos = (1275, -400)
    objectSize = (100, 50)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Walljump platform 2.
    objectPos = (925, -600)
    objectSize = (100, 50)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Walljump platform 3.
    objectPos = (1275, -750)
    objectSize = (100, 50)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Upper section block before big jump.
    objectPos = (-275, -1200)
    objectSize = (200, 400)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Upper section first stair.
    objectPos = (525, -1000)
    objectSize = (300, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Upper section second stair.
    objectPos = (425, -1100)
    objectSize = (200, 300)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Upper section floor.
    objectPos = (-275, -900)
    objectSize = (1225, 100)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left wall for walljump.
    objectPos = (925, -900)
    objectSize = (50, 500)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Final platform.
    objectPos = (-1375, -1200)
    objectSize = (600, 400)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left platform.
    objectPos = (-1375, -100)
    objectSize = (700, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Right border.
    objectPos = (1325, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left border.
    objectPos = (-1975, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Floor.
    objectPos = (-1835, 180)
    objectSize = (4000, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Parkour platform 1.
    objectPos = (-375, -150)
    objectSize = (200, 50)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Parkour platform 2.
    objectPos = (0, -150)
    objectSize = (200, 50)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Parkour platform 3.
    objectPos = (375, -150)
    objectSize = (200, 50)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # End door.
    objectPos = (-950, -1350)
    objectSize = (100, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_2", "Door", ("Sprites/door.png", ButtonFunctions.ToWorld_1), 0, 3, [0])
    result["Door"].append(gameObject)

    return result

def Level_3():
    """ Adds the Level_0 pooler (= the playtest level) to the main pooler. """
    global initDictionary
    result = CopyDict(initDictionary)

    wallTexture = "Sprites/wall.png"

    # Right border.
    objectPos = (1660, -2700)
    objectSize = (500, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Floor.
    objectPos = (-940, 180)
    objectSize = (Constants.screenDimensions[0] * 5, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left border.
    objectPos = (-1640, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_3", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    return result

def Level_4():
    global initDictionary
    result = CopyDict(initDictionary)

    wallTexture = "Sprites/wall.png"

    # Right border.
    objectPos = (1660, -2700)
    objectSize = (500, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_4", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Floor.
    objectPos = (-940, 180)
    objectSize = (Constants.screenDimensions[0] * 5, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_4", "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left border.
    objectPos = (-1640, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Level_4", "Real", wallTexture, 0, 2, [0])
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