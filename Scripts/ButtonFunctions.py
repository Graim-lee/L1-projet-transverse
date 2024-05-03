""" ##################################################
    Every function that will be executed when a
    button is clicked is located here.
 ################################################# """

import Scripts.Constants as Constants
import Scripts.Object as Object
import Scripts.Level as Level
import Scripts.Animations as Animations

player: Object.GameObject

def SetPlayer(setPlayer: Object.GameObject):
    """ Allows to cache the player game object for future uses. """
    global player
    player = setPlayer

def ToMainMenu():
    Constants.currentWorld = "Main_Menu"
    Constants.currentScene = "Main_Menu"

def PauseToMainMenu():
    Level.ResetScene(Constants.currentLevel)
    Constants.currentWorld = "Main_Menu"
    Constants.currentScene = "Main_Menu"

def Continue():
    Constants.currentScene = Constants.currentLevel

def Restart():
    Level.ResetScene(Constants.currentLevel)
    Constants.currentScene = Constants.currentLevel
    player.position = Object.Vector2(0, 0)

def ToWorldSelection():
    Constants.currentWorld = "Main_Menu"
    Constants.currentScene = "World_Selection"

def ToWorldSelectionMenu():
    Level.ResetScene(Constants.currentLevel)
    Constants.currentWorld = "Main_Menu"
    Constants.currentScene = "World_Selection"
    Level.ResetScene(Constants.currentScene)

def ToExtraMenu():
    Constants.currentWorld = "Main_Menu"
    Constants.currentScene = "Extra_Menu"

def ToCloset():
    Constants.currentWorld = "Main_Menu"
    Constants.currentScene = "Closet_Menu"

def ToChangeSkinRight():
    """
        This function find the next Skin to his right (in list and display), update the skin display in the menu with UpdateDisplaySkin()
        Finally change the skin with his next skin on his right side
    """
    index = Constants.skinList.index(Constants.skin)
    if index + 1 == len(Constants.skinList):
        newSkin = Constants.skinList[0]
    else:
        newSkin = Constants.skinList[index + 1]
    Constants.currentWorld = "Main_Menu"
    UpdateDisplaySkin(newSkin)
    Constants.skin = newSkin

def ToChangeSkinLeft():
    """
        This function find the next Skin to his left (in list and display), update the skin display in the menu with UpdateDisplaySkin()
        Finally change the skin with his next skin on his left side
    """
    index = Constants.skinList.index(Constants.skin)
    if index - 1 == -1:
        newSkin = Constants.skinList[len(Constants.skinList) - 1]
    else:
        newSkin = Constants.skinList[index - 1]
    Constants.currentWorld = "Main_Menu"
    UpdateDisplaySkin(newSkin)
    Constants.skin = newSkin

def UpdateDisplaySkin(skin : (str)):
    """
        This function update the skin display on the menu by looking at every sprite in the pooler (to reduce the range we only look in Text where there is all the skin only
        Then we compare his data to the value of the new skin and update the skin to selected.png otherwise, we update the skin to idle.png so we see what we have selected
        We resize to fit well on the screen otherwise size = (44,44)
        Args:
            - skin : (str) the new skin find thanks to ToChangeSkinLeft/Right()
    """
    for gameObject in Constants.objectsInScene["Text"]:
        if gameObject.data == "Sprites/Player/" + skin + "/idle.png" or gameObject.data == "Sprites/Player/" + skin + "/selected.png":
            gameObject.SetSprite("Sprites/Player/" + skin + "/selected.png", False)
            gameObject.Resize((201,201))
        else:
            listData = gameObject.data.split("/")
            gameObject.SetSprite("Sprites/Player/" + listData[2] + "/idle.png", False)
            gameObject.Resize((201, 201))
    Constants.currentWorld = "Main_Menu"

def UpdateCoin():
    """
    This function update the text of coin counter
    :return:
    """
    for gameObject in Constants.objectsInScene["Text"]:
        if gameObject.data[0] == str(Constants.coin_counter -1)+" /20":
            gameObject.data = (str(Constants.coin_counter)+" /20", True)

def ToLootBox():
    """
        This function Should display on a new scene the animation of an box opening, for example like brawl star with the background color of the player color
        But I still don't figured out how to do it
    """
    Constants.currentScene = "Loot_Box"
    Constants.inMenu = False
    Constants.currentWorld = "Main_Menu"

def ToCredit():
    Constants.currentWorld = "Main_Menu"
    Constants.currentScene = "Credit_Menu"

def ToWorld_1():
    Constants.currentScene = "Main_Menu"
    Constants.currentScene = "World_1"

def ToLevel_World1():
    Constants.currentScene = "Level_World_1"
    Constants.currentLevel = "Level_World_1"
    Constants.currentWorld = "World_1"
    player.position = Object.Vector2(0, 0)

def ToLevel_1_1():
    Constants.currentScene = "Level_1_1"
    Constants.currentLevel = "Level_1_1"
    Constants.currentWorld = "World_1"
    player.position = Object.Vector2(0, 0)

def ToLevel_1_2():
    Constants.currentScene = "Level_1_2"
    Constants.currentLevel = "Level_1_2"
    Constants.currentWorld = "World_1"
    player.position = Object.Vector2(0, 0)

def ToLevel_1_3():
    Constants.currentScene = "Level_1_3"
    Constants.currentLevel = "Level_1_3"
    Constants.currentWorld = "World_1"
    player.position = Object.Vector2(0, 0)

def ToLevel_1_4():
    Constants.currentScene = "Level_1_4"
    Constants.currentLevel = "Level_1_4"
    Constants.currentWorld = "World_1"
    player.position = Object.Vector2(0, 0)

def ToWorld_2():
    Constants.currentScene = "Main_Menu"
    Constants.currentScene = "World_2"

def ToLevel_2_1():
    Constants.currentScene = "Level_2_1"
    Constants.currentLevel = "Level_2_1"
    Constants.currentWorld = "World_2"
    player.position = Object.Vector2(0, 0)

def ToLevel_2_2():
    Constants.currentScene = "Level_2_2"
    Constants.currentLevel = "Level_2_2"
    Constants.currentWorld = "World_2"
    player.position = Object.Vector2(0, 0)

def ToLevel_2_3():
    Constants.currentScene = "Level_2_3"
    Constants.currentLevel = "Level_2_3"
    Constants.currentWorld = "World_2"
    player.position = Object.Vector2(0, 0)

def ToWorld_3():
    Constants.groundedFrictionCoeff = 0.7
    Constants.currentScene = "Main_Menu"
    Constants.currentScene = "World_3"

def ToLevel_3_1():
    Constants.currentScene = "Level_3_1"
    Constants.currentLevel = "Level_3_1"
    Constants.currentWorld = "World_3"
    player.position = Object.Vector2(0, 0)

def ToLevel_3_2():
    Constants.currentScene = "Level_3_2"
    Constants.currentLevel = "Level_3_2"
    Constants.currentWorld = "World_3"
    player.position = Object.Vector2(0, 0)

def ToLevel_3_3():
    Constants.currentScene = "Level_3_3"
    Constants.currentLevel = "Level_3_3"
    Constants.currentWorld = "World_3"
    player.position = Object.Vector2(0, 0)

def ToLevel_3_4():
    Constants.currentScene = "Level_3_4"
    Constants.currentLevel = "Level_3_4"
    Constants.currentWorld = "World_3"
    player.position = Object.Vector2(0, 0)

def EndLevel():
    Constants.currentScene = "World_Selection"
    Constants.currentScene = "Main_Menu"
    Level.ResetScene(Constants.currentLevel)
    ToWorldSelection()

def QuitGame():
    Constants.gameRunning = False