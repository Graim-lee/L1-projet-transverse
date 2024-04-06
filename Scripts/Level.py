import pygame
import Scripts.Constants as Constants
import Scripts.Physics as Physics
import Scripts.InputsManager as InputsManager
import Scripts.Object as Object
import Scripts.ButtonFunctions as ButtonFunctions
import random

initPooler = Object.Pooler()
initDictionary = {"Door": [], "Water": [], "Wall": [], "Text": [], "Trajectory": [], "Button": [], "Player": [], "Throwable": []}

mainPooler: Object.Pooler

def GetPooler() -> Object.Pooler:
    """ Returns the whole game's pooler by calling each scene's pooler individually. I checked for performance issues,
     and it seems that having that many objects at the same time in the pooler isn't bad. What matters is how many objects
     are on-screen at the same time. """
    global mainPooler
    pooler = initPooler.Copy()

    # We individually initiate each of the game's scene in the pooler.
    pooler.SetScene("Level_All", All())
    pooler.SetScene("Main_Menu", MainMenu())
    pooler.SetScene("Pause_Menu", PauseMenu())
    pooler.SetScene("World_Selection", WorldSelection())

    pooler.SetScene("World_1", World_1())
    pooler.SetScene("Level_1_1", Level_1_1())
    pooler.SetScene("Level_1_2", Level_1_2())
    pooler.SetScene("Level_1_3", Level_1_3())
    pooler.SetScene("Level_1_4", Level_1_4())

    pooler.SetScene("World_2", World_2())
    pooler.SetScene("Level_2_1", Level_2_1())
    pooler.SetScene("Level_2_2", Level_2_2())

    pooler.SetScene("World_3", World_3())
    pooler.SetScene("Level_3_1", Level_3_1())
    pooler.SetScene("Level_3_2", Level_3_2())
    pooler.SetScene("Level_3_3", Level_3_3())
    pooler.SetScene("Level_3_4", Level_3_4())

    pooler.SetScene("Extra_Menu", ExtraMenu())
    pooler.SetScene("Closet_Menu", ClosetMenu())
    pooler.SetScene("Loot_Box", LootBox())
    pooler.SetScene("Credit_Menu", CreditMenu())

    pooler.SetScene("Level_World_Selection", LevelWorldSelection())
    pooler.SetScene("Level_World_1", LevelWorld_1())

    mainPooler = pooler
    return pooler

def ResetScene(scene: str):
    """ Resets the given scene. As said above, it apparently does not cause any memory leak. """
    global mainPooler
    for category in mainPooler.main[scene]:
        for gameObject in mainPooler.main[scene][category]:
            gameObject.position = gameObject.initialPosition

def All():
    """ Adds the objects that are always loaded to the pooler. """
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    # Player.
    playerSize = (44, 44)
    playerTexture = "Sprites/Player/blue/idle.png"
    gameObject = Object.GameObject((0,0), playerSize, "Real", playerTexture, 1, 1, [0, 3, 5], True, True, True)
    result["Player"].append(gameObject)

    # Trajectory dots.
    for i in range(5):
        gameObject = Object.GameObject((0, 0), (10 - i, 10 - i), "Real", "Sprites/dot.png", 0, 0, [0, 1, 2, 3, 4])
        gameObject.active = False
        result["Trajectory"].append(gameObject)

    return result

def MainMenu():
    """ Adds the Main Menu pooler to the main pooler. """
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    # Title of the game.
    objectPos = (Constants.screenDimensions[0] / 2, 270)
    gameObject = Object.GameObject(objectPos, (0,0), "Text", ("Penguin Run", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # "Play game" button.
    objectPos = (Constants.screenDimensions[0] / 2, 500)
    gameObject = Object.GameObject(objectPos, (160, 70), "Button", ("Play", ButtonFunctions.ToWorldSelection), 0, 0, [0])
    result["Button"].append(gameObject)

    # "World selection test menu" button.
    objectPos = (Constants.screenDimensions[0] / 2, 625)
    gameObject = Object.GameObject(objectPos, (340, 70), "Button", ("World select", ButtonFunctions.ToLevel_WorldSelection), 0, 0, [0])
    result["Button"].append(gameObject)

    # "ExtraMenu" button.
    objectPos = (Constants.screenDimensions[0] / 2 + 400, 700)
    gameObject = Object.GameObject(objectPos, (160, 70), "Button",("Extra", ButtonFunctions.ToExtraMenu), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Quit game" button.
    objectPos = (Constants.screenDimensions[0] / 2, 770)
    gameObject = Object.GameObject(objectPos, (160, 70), "Button", ("Quit", ButtonFunctions.QuitGame), 0, 0, [0])
    result["Button"].append(gameObject)

    # Penguin sprite on the left of the screen
    objectPos = (Constants.screenDimensions[0] / 2 - 500, 450)
    gameObject = Object.GameObject(objectPos, (200,200),"Real", "Sprites/Player/"+Constants.skin+"/idle.png", 0, 0, [0],True,True,False)
    result["Text"].append(gameObject)

    # Penguin sprite on the right of the screen
    objectPos = (Constants.screenDimensions[0] / 2 + 300, 450)
    gameObject = Object.GameObject(objectPos, (200,200),"Real", "Sprites/Player/"+Constants.skin+"/idle.png", 0, 0, [0],True,True,False)
    gameObject.surface = pygame.transform.flip(gameObject.surface, True, False)
    result["Text"].append(gameObject)

    return result

def PauseMenu():
    """ Adds the Pause Menu pooler to the main pooler. """
    result = CopyEmptyDict(initDictionary)

    # Title ("Pause").
    objectPos = (Constants.screenDimensions[0] / 2, 270)
    gameObject = Object.GameObject(objectPos, (0, 0), "Text", ("Pause", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # ESC to restart the game
    objectPos = (Constants.screenDimensions[0] / 2, 400)
    gameObject = Object.GameObject(objectPos, (0, 0),  "Text", ("Press ESC to get back to the game", False), 0, 0, [0])
    result["Text"].append(gameObject)

    # "Back to menu" button.
    objectPos = (Constants.screenDimensions[0] / 2 + 250, 650)
    gameObject = Object.GameObject(objectPos, (350, 80), "Button", ("Back to menu", ButtonFunctions.PauseToMainMenu), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Continue" button.
    objectPos = (Constants.screenDimensions[0] / 2 - 250, 650)
    gameObject = Object.GameObject(objectPos, (350, 80), "Button", ("Continue",ButtonFunctions.Continue), 0,0, [0])
    result["Button"].append(gameObject)

    # "Restart" button.
    objectPos = (Constants.screenDimensions[0] / 2, 550)
    gameObject = Object.GameObject(objectPos, (350, 80), "Button", ("Restart", ButtonFunctions.Restart), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Quit game" button.
    objectPos = (Constants.screenDimensions[0] / 2, 770)
    gameObject = Object.GameObject(objectPos, (160, 70), "Button", ("Quit", ButtonFunctions.QuitGame), 0, 0, [0])
    result["Button"].append(gameObject)

    return result

def LevelWorldSelection():
    """ Adds the World Selection lobby to the main pooler. """
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    wallTexture = "Sprites/wall.png"
    doorTexture = "Sprites/door.png"

    # World 1 door.
    objectPos = (490, -70)
    objectSize = (100, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Door", (doorTexture, ButtonFunctions.ToLevel_World1), 0, 3, [0])
    result["Door"].append(gameObject)

    # World 1 door "WORLD 1" text.
    objectPos = (540, -120)
    gameObject = Object.GameObject(objectPos, (0, 0), "Text", ("WORLD 1", False), 0, 0, [0])
    result["Text"].append(gameObject)

    # Floor.
    objectPos = (-960, 80)
    objectSize = (Constants.screenDimensions[0] * 5, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    return result

def LevelWorld_1():
    """ Adds the World 1 lobby pooler to the main pooler. """
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    wallTexture = "Sprites/wall.png"

    # Floor.
    objectPos = (-960, 80)
    objectSize = (1000, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    return result

def WorldSelection():
    """ Adds the World Selection pooler to the main pooler. """
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    # Title "World selection".
    objectPos = (Constants.screenDimensions[0] / 2, 240)
    gameObject = Object.GameObject(objectPos, (0,0), "Text", ("World selection", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # "World 1" button.
    objectPos = (1 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2 - 100)
    gameObject = Object.GameObject(objectPos, (200, 200), "WorldButton", ("WORLD 1", ButtonFunctions.ToWorld_1, "Sprites/Worlds/world1.png"), 0, 0, [0])
    result["Button"].append(gameObject)

    # "World 2" button.
    objectPos = (2 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2 - 100)
    gameObject = Object.GameObject(objectPos, (200, 200), "WorldButton",("WORLD 2", ButtonFunctions.ToWorld_2, "Sprites/Worlds/world1.png"), 0, 0, [0])
    result["Button"].append(gameObject)

    # "World 3" button.
    objectPos = (3 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2 - 100)
    gameObject = Object.GameObject(objectPos, (200, 200), "WorldButton",("WORLD 3", ButtonFunctions.ToWorld_3, "Sprites/Worlds/world1.png"), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Quit Game" button.
    objectPos = (Constants.screenDimensions[0] / 2, 900)
    gameObject = Object.GameObject(objectPos, (160, 70), "Button", ("Quit", ButtonFunctions.QuitGame), 0, 0, [0])
    result["Button"].append(gameObject)

    return result

def World_1():
    """ Adds the World 1 level selection menu pooler to the main pooler. """
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    # Title "World 1".
    objectPos = (Constants.screenDimensions[0] / 2, 240)
    gameObject = Object.GameObject(objectPos, (0,0), "Text", ("World 1", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # "Level 1" button.
    objectPos = (1 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    gameObject = Object.GameObject(objectPos, (200, 160), "Button", ("Level 1", ButtonFunctions.ToLevel_1_1), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Level 2" button.
    objectPos = (2 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    gameObject = Object.GameObject(objectPos, (200, 160), "Button", ("Level 2", ButtonFunctions.ToLevel_1_2), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Level 3" button.
    objectPos = (3 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    gameObject = Object.GameObject(objectPos, (200, 160), "Button", ("Level 3", ButtonFunctions.ToLevel_1_3), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Level 4" Button.
    objectPos = (4 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    gameObject = Object.GameObject(objectPos, (200, 160), "Button", ("Level 4", ButtonFunctions.ToLevel_1_4), 0, 0, [0])
    result["Button"].append(gameObject)

    return result

def Level_1_1():
    """ Adds the Level_0 pooler (= the playtest level) to the main pooler. """
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    Constants.groundedFrictionCoeff = 0.7

    wallTexture = "Sprites/wall.png"

    # Little block.
    objectPos = (250, 80)
    objectSize = (100, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Big block.
    objectPos = (900, -20)
    objectSize = (100, 300)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Final platform.
    objectPos = (1400, -200)
    objectSize = (400, 100)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Right border.
    objectPos = (1660, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left border.
    objectPos = (-1200, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Floor.
    objectPos = (-1800, 180)
    objectSize = (5000, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # End door.
    objectPos = (1500, -400)
    objectSize = (100, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Door", ("Sprites/door.png", ButtonFunctions.EndLevel), 0, 3, [0])
    result["Door"].append(gameObject)

    return result

def Level_1_2():
    """ Adds the Level_0 pooler (= the playtest level) to the main pooler. """
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    Constants.groundedFrictionCoeff = 0.7

    wallTexture = "Sprites/wall.png"

    # Left stair n°2.
    objectPos = (-775, -20)
    objectSize = (200, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left stair n°1.
    objectPos = (-775, 80)
    objectSize = (300, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Right platform.
    objectPos = (725, -200)
    objectSize = (700, 500)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Walljump platform 1.
    objectPos = (1275, -400)
    objectSize = (100, 50)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Walljump platform 2.
    objectPos = (925, -600)
    objectSize = (100, 50)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Walljump platform 3.
    objectPos = (1275, -750)
    objectSize = (100, 50)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Upper section block before big jump.
    objectPos = (-275, -1200)
    objectSize = (200, 400)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Upper section first stair.
    objectPos = (525, -1000)
    objectSize = (300, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Upper section second stair.
    objectPos = (425, -1100)
    objectSize = (200, 300)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Upper section floor.
    objectPos = (-275, -900)
    objectSize = (1225, 100)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left wall for walljump.
    objectPos = (925, -900)
    objectSize = (50, 500)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Final platform.
    objectPos = (-1375, -1200)
    objectSize = (600, 400)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left platform.
    objectPos = (-1375, -100)
    objectSize = (700, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Right border.
    objectPos = (1325, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left border.
    objectPos = (-1975, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Floor.
    objectPos = (-1835, 180)
    objectSize = (4000, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Parkour platform 1.
    objectPos = (-375, -150)
    objectSize = (200, 50)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Parkour platform 2.
    objectPos = (0, -150)
    objectSize = (200, 50)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Parkour platform 3.
    objectPos = (375, -150)
    objectSize = (200, 50)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # End door.
    objectPos = (-950, -1400)
    objectSize = (100, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Door", ("Sprites/door.png", ButtonFunctions.EndLevel), 0, 3, [0])
    result["Door"].append(gameObject)

    return result

def Level_1_3():
    """ Adds the Level_0 pooler (= the playtest level) to the main pooler. """
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    Constants.groundedFrictionCoeff = 0.7

    wallTexture = "Sprites/wall.png"

    # Right platform.
    objectPos = (600, -150)
    objectSize = (500, 500)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left stair.
    objectPos = (-300, 200)
    objectSize = (200, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left platform.
    objectPos = (-700, 100)
    objectSize = (500, 300)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Final platform.
    objectPos = (-20, -600)
    objectSize = (600, 50)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Ceiling.
    objectPos = (-1800, -2700)
    objectSize = (5000, 1750)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Upper left wall.
    objectPos = (-700, -2700)
    objectSize = (800, 2149)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Right border.
    objectPos = (960, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left border.
    objectPos = (-1600, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Floor.
    objectPos = (-1800, 300)
    objectSize = (5000, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # End door.
    objectPos = (200, -800)
    objectSize = (100, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Door", ("Sprites/door.png", ButtonFunctions.EndLevel), 0, 3, [0])
    result["Door"].append(gameObject)

    return result

def Level_1_4():
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    Constants.groundedFrictionCoeff = 0.7


    wallTexture = "Sprites/wall.png"

    # Right border.
    objectPos = (1660, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left border.
    objectPos = (-1200, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Bottom.
    objectPos = (100, 300)
    objectSize = (2000, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Water.
    objectPos = (100, 200)
    objectSize = (500, 250)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", "Sprites/Water/water_1.png", 0, 4, [0, 1], _png=True, _hasAnimation=True)
    result["Water"].append(gameObject)

    # Floor.
    objectPos = (-1800, 180)
    objectSize = (2000, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    return result

def World_2():
    """ Adds the World 2 level selection menu pooler to the main pooler. """
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    # Title "Here you can only slide !".
    objectPos = (Constants.screenDimensions[0] / 2, 720)
    gameObject = Object.GameObject(objectPos, (0, 0), "Text", ("Here you can only ", True), 0, 0, [0])
    result["Text"].append(gameObject)
    objectPos = (Constants.screenDimensions[0] / 2 , 820)
    gameObject = Object.GameObject(objectPos, (0, 0), "Text", ("Slide !", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # Title "World 2".
    objectPos = (Constants.screenDimensions[0] / 2, 240)
    gameObject = Object.GameObject(objectPos, (0,0), "Text", ("World 2", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # "Level 1" button.
    objectPos = (1 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    gameObject = Object.GameObject(objectPos, (200, 160), "Button", ("Level 1", ButtonFunctions.ToLevel_2_1), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Level 2" button.
    objectPos = (2 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    gameObject = Object.GameObject(objectPos, (200, 160), "Button", ("Level 2", ButtonFunctions.ToLevel_2_2), 0, 0, [0])
    result["Button"].append(gameObject)

    return result

def Level_2_1():
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    wallTexture = "Sprites/wall.png"
    iceTexture = "Sprites/ice.png"
    iceWallTexture = "Sprites/iceWall.png"

    # Floor.
    objectPos = (-1800, 200)
    objectSize = (5000, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left border.
    objectPos = (-1200, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Bloc 1 platform.
    objectPos = (400, 100)
    objectSize = (800, 100)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Bloc 2 platform.
    objectPos = (1000, 0)
    objectSize = (400, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Right platform.
    objectPos = (1600, -2000)
    objectSize = (500, 2000)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceWallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Right top.
    objectPos = (-200, -500)
    objectSize = (1800, 100)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Transition section.
    # Block 1
    objectPos = (2200, 100)
    objectSize = (600, 100)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Block 2
    objectPos = (2650,  0)
    objectSize = (500, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Block Small border
    objectPos = (3150, -300)
    objectSize = (50, 500)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceWallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Block up left.
    objectPos = (2100, -200)
    objectSize = (600, 75)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Block up right
    objectPos = (2900, -350)
    objectSize = (600, 75)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Floor.
    objectPos = (3100, 300)
    objectSize = (5000, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Block on floor.
    objectPos = (3200, 100)
    objectSize = (300, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Block up right
    objectPos = (3700, -150)
    objectSize = (400, 100)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Block Small border
    objectPos = (3900, -50)
    objectSize = (100, 350)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceWallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Block up right
    objectPos = (4200, 0)
    objectSize = (900, 100)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Block Small wall1.
    objectPos = (4300, 100)
    objectSize = (100, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceWallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Block Small wall2.
    objectPos = (4900, 100)
    objectSize = (100, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceWallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Block floor.
    objectPos = (5000, 150)
    objectSize = (900, 150)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", iceTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Right border.
    objectPos = (5900, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # End door.
    objectPos = (5600, -50)
    objectSize = (100, 200)
    gameObject = Object.GameObject(objectPos, objectSize, "Door", ("Sprites/door.png", ButtonFunctions.EndLevel), 0, 3,[0])
    result["Door"].append(gameObject)

    return result

def Level_2_2():
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    return result

def World_3():
    """ Adds the World 1 level selection menu pooler to the main pooler. """
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    # Title "World 3".
    objectPos = (Constants.screenDimensions[0] / 2, 240)
    gameObject = Object.GameObject(objectPos, (0,0), "Text", ("World 3", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # "Level 1" button.
    objectPos = (1 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    gameObject = Object.GameObject(objectPos, (200, 160), "Button", ("Level 1", ButtonFunctions.ToLevel_3_1), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Level 2" button.
    objectPos = (2 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    gameObject = Object.GameObject(objectPos, (200, 160), "Button", ("Level 2", ButtonFunctions.ToLevel_3_2), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Level 3" button.
    objectPos = (3 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    gameObject = Object.GameObject(objectPos, (200, 160), "Button", ("Level 3", ButtonFunctions.ToLevel_3_3), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Level 4" Button.
    objectPos = (4 * Constants.screenDimensions[0] / 5, Constants.screenDimensions[1] / 2)
    gameObject = Object.GameObject(objectPos, (200, 160), "Button", ("Level 4", ButtonFunctions.ToLevel_3_4), 0, 0, [0])
    result["Button"].append(gameObject)

    return result

def Level_3_1():
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    wallTexture = "Sprites/wall.png"

    # Floor.
    objectPos = (-1800, 180)
    objectSize = (5000, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left border.
    objectPos = (-1200, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Right platform.
    objectPos = (725, 100)
    objectSize = (200, 10)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Football.
    objectPos = (200, -100)
    objectSize = (32, 32)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", "Sprites/football.png", 1, 5, [0, 1], _png=True)
    result["Throwable"].append(gameObject)

    return result

def Level_3_2():
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    wallTexture = "Sprites/wall.png"

    # Floor.
    objectPos = (-1800, 180)
    objectSize = (5000, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left border.
    objectPos = (-1200, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Right platform.
    objectPos = (725, 100)
    objectSize = (200, 10)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    return result

def Level_3_3():
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    wallTexture = "Sprites/wall.png"

    # Floor.
    objectPos = (-1800, 180)
    objectSize = (5000, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left border.
    objectPos = (-1200, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Right platform.
    objectPos = (725, 100)
    objectSize = (200, 10)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    return result

def Level_3_4():
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    wallTexture = "Sprites/wall.png"

    # Floor.
    objectPos = (-1800, 180)
    objectSize = (5000, 800)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Left border.
    objectPos = (-1200, -2700)
    objectSize = (1000, 4000)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    # Right platform.
    objectPos = (725, 100)
    objectSize = (200, 10)
    gameObject = Object.GameObject(objectPos, objectSize, "Real", wallTexture, 0, 2, [0])
    result["Wall"].append(gameObject)

    return result

def CopyEmptyDict(dictionary: {}) -> {}:
    """ Returns an UNLINKED copy of the given dictionary, meaning changing the value of the new dictionary (the copy)
    won't affect the initial dictionary. The given dictionary must be empty, that is of the form {name_of_category: []}.
        Args:
            - dictionary ({str: []}): the dictionary to copy.
        Returns:
            - ({str: []}): a copy of the dictionary.
    """
    result = {}
    for category in dictionary:
        result[category] = []
    return result

def ExtraMenu():
    """ Adds the Skin Menu Selection lobby to the main pooler. """
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    # Hanger sprite on the left of the screen
    objectPos = (Constants.screenDimensions[0] / 2 - 500, 400)
    game0bject = Object.GameObject(objectPos, (200, 200), "Real", "Sprites/hanger.png", 0, 0, [0], True, True,False)
    result["Text"].append(game0bject)

    # Change skin button.
    objectPos = (Constants.screenDimensions[0] / 2 - 400, 725)
    gameObject = Object.GameObject(objectPos, (160, 70), "Button", ("Change", ButtonFunctions.ToCloset), 0, 0, [0])
    result["Button"].append(gameObject)

    # Open button.
    # ToLootBox not finish.
    objectPos = (Constants.screenDimensions[0] / 2, 625)
    gameObject = Object.GameObject(objectPos, (340, 70), "Button", ("Open", ButtonFunctions.ToLootBox), 0,0, [0])
    result["Button"].append(gameObject)

    # Chest in the middle the screen.
    objectPos = (Constants.screenDimensions[0] / 2 - 100, 350)
    gameObject = Object.GameObject(objectPos, (200, 200), "Real", "Sprites/Chest.png", 0, 0, [0], True, True,False)
    result["Text"].append(gameObject)

    # Setting sprite on the left of the screen
    objectPos = (Constants.screenDimensions[0] / 2 + 300, 400)
    game0bject = Object.GameObject(objectPos, (200, 200), "Real", "Sprites/Setting.png", 0, 0, [0], True, True, False)
    result["Text"].append(game0bject)

    # Credit skin button.
    objectPos = (Constants.screenDimensions[0] / 2 + 400, 725)
    gameObject = Object.GameObject(objectPos, (160, 70), "Button", ("Credit", ButtonFunctions.ToCredit), 0, 0, [0])
    result["Button"].append(gameObject)

    # "Return" button.
    objectPos = (Constants.screenDimensions[0] / 2, 900)
    gameObject = Object.GameObject(objectPos, (160, 70), "Button", ("Return", ButtonFunctions.ToMainMenu), 0, 0, [0])
    result["Button"].append(gameObject)

    return result

def ClosetMenu():
    """ Adds the Skin Menu Selection lobby to the main pooler. """
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    # Change skin to the right button.
    objectPos = (Constants.screenDimensions[0] / 2 + 50, 725)
    gameObject = Object.GameObject(objectPos, (70, 70), "Button", (">", ButtonFunctions.ToChangeSkinRight), 0, 0, [0])
    result["Button"].append(gameObject)

    # Change skin to the left button.
    objectPos = (Constants.screenDimensions[0] / 2 - 50, 725)
    gameObject = Object.GameObject(objectPos, (70, 70), "Button", ("<", ButtonFunctions.ToChangeSkinLeft), 0, 0,[0])
    result["Button"].append(gameObject)

    # Penguin black sprite on the left of the screen
    objectPos = (Constants.screenDimensions[0] / 2 - 500, 450)
    gameObject = Object.GameObject(objectPos, (200, 200), "Real", "Sprites/Player/black/idle.png", 0, 0, [0], True,True, False)
    result["Text"].append(gameObject)

    # Penguin blue sprite on the right of the screen
    objectPos = (Constants.screenDimensions[0] / 2 + 300, 450)
    gameObject = Object.GameObject(objectPos, (200, 200), "Real", "Sprites/Player/blue/selected.png", 0,0, [0], True, True, False)
    result["Text"].append(gameObject)

    # Penguin Iren sprite on the left of the screen
    objectPos = (Constants.screenDimensions[0] / 2 - 100, 450)
    gameObject = Object.GameObject(objectPos, (200, 200), "Real", "Sprites/Player/Iren/idle.png", 0, 0, [0],True, True, False)
    result["Text"].append(gameObject)

    # "Select skin button.
    objectPos = (Constants.screenDimensions[0] / 2, 900)
    gameObject = Object.GameObject(objectPos, (160, 70), "Button", ("Select", ButtonFunctions.ToExtraMenu), 0, 0, [0])
    result["Button"].append(gameObject)

    return result

def CreditMenu():
    """ Adds the Setting Menu to the Extra lobby to the main pooler. """
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    # Credit of the game.
    objectPos = (Constants.screenDimensions[0] / 2, 290)
    gameObject = Object.GameObject(objectPos, (0, 0), "Text", ("______", True), 0, 0, [0])
    result["Text"].append(gameObject)
    # Credit of the game.
    objectPos = (Constants.screenDimensions[0] / 2, 270)
    gameObject = Object.GameObject(objectPos, (0, 0), "Text", ("Credit", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # Antoine.
    objectPos = (Constants.screenDimensions[0] / 2, 400)
    gameObject = Object.GameObject(objectPos, (0, 0), "Text", ("- Antoine", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # Jeremy .
    objectPos = (Constants.screenDimensions[0] / 2, 500)
    gameObject = Object.GameObject(objectPos, (0, 0), "Text", ("- Jeremy", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # Léandre .
    objectPos = (Constants.screenDimensions[0] / 2, 600)
    gameObject = Object.GameObject(objectPos, (0, 0), "Text", ("- Leandre", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # Matthieu
    objectPos = (Constants.screenDimensions[0] / 2, 700)
    gameObject = Object.GameObject(objectPos, (0, 0), "Text", ("- Matthieu", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # Rémi
    objectPos = (Constants.screenDimensions[0] / 2, 800)
    gameObject = Object.GameObject(objectPos, (0, 0), "Text", ("- Remi", True), 0, 0, [0])
    result["Text"].append(gameObject)

    # "Return" button.
    objectPos = (Constants.screenDimensions[0] / 2, 900)
    gameObject = Object.GameObject(objectPos, (160, 70), "Button", ("Return", ButtonFunctions.ToExtraMenu), 0, 0, [0])
    result["Button"].append(gameObject)

    return result
def LootBox():
    # scene not finish at all
    """ Adds the LootBox Menu Selection lobby to the main pooler. """
    global initDictionary
    result = CopyEmptyDict(initDictionary)

    # Animation of the open  box in the middle the screen
    objectPos = (Constants.screenDimensions[0] / 2 - 150, 450)
    gameObject = Object.GameObject(objectPos, (350, 500), "Real", "Sprites/Chest_open.png", 0, 0, [0], True, True, False)
    result["Text"].append(gameObject)


    return result

def CopyFullDict(dictionary: {}) -> {}:
    """ Same as the last function, but with a filled dictionary, that is, a dictionary of the form
    {name_of_category: list_of_objects}. I created two functions as this one is a little bit slower to run (so using the
    first one when possible saves performances).
        Args:
            - dictionary ({str: [GameObject]}): the dictionary to copy.
        Returns:
            - ({str: [GameObject]}): a copy of the given dictionary.
    """
    result = {}
    for category in dictionary:
        result[category] = []
    return result

""" LIST OF EVERY SCENE :

    - Main_Menu: the base scene (the one in which we are when we start the game), the main menu.
    - World_Selection: the world selection scene. Accessible after clicking on "Play" in the main menu.
    - World_1: the level selection menu of world 1.
    - Pause_Menu: the pause menu.
    
    - Level_0: the playtest level.

"""