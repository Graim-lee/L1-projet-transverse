""" ##################################################
    Every function that will be executed when a
    button is clicked is located here.
 ################################################# """

import Scripts.Constants as Constants
import Scripts.Object as Object
import Scripts.Level as Level

player: Object.GameObject

def SetPlayer(setPlayer: Object.GameObject):
    """ Allows to cache the player game object for future uses. """
    global player
    player = setPlayer

def PauseToMainMenu():
    Level.ResetScene(Constants.currentLevel)
    Constants.currentScene = "Main_Menu"

def ToMainMenu():
    Constants.currentScene = "Main_Menu"

def ToWorldSelection():
    Constants.currentScene = "World_Selection"

def ToSkinMenu():
    Constants.currentScene = "Skin_Menu"

def ToCloset():
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
            gameObject.SetSprite("Sprites/Player/" + skin + "/selected.png")
            gameObject.Resize((201,201))
        else:
            listData = gameObject.data.split("/")
            gameObject.SetSprite("Sprites/Player/" + listData[2] + "/idle.png")
            gameObject.Resize((201, 201))

def ToLootBox():
    """
        This function Should display on a new scene the animation of an box opening, for example like brawl star with the background color of the player color
        But I still don't figured out how to do it
    """
    Constants.currentScene = "Loot_Box"

def ToLevel_WorldSelection():
    Constants.currentScene = "Level_World_Selection"
    Constants.currentLevel = "Level_World_Selection"
    player.position = Object.Vector2(0, 0)

def ToWorld_1():
    Constants.currentScene = "World_1"

def ToLevel_World1():
    Constants.currentScene = "Level_World_1"
    Constants.currentLevel = "Level_World_1"
    player.position = Object.Vector2(0, 0)

def ToLevel_1_1():
    Constants.currentScene = "Level_1_1"
    Constants.currentLevel = "Level_1_1"
    player.position = Object.Vector2(0, 0)

def ToLevel_1_2():
    Constants.currentScene = "Level_1_2"
    Constants.currentLevel = "Level_1_2"
    player.position = Object.Vector2(0, 135)

def ToLevel_1_3():
    Constants.currentScene = "Level_1_3"
    Constants.currentLevel = "Level_1_3"
    player.position = Object.Vector2(300, 250)

def ToLevel_1_4():
    Constants.currentScene = "Level_1_4"
    Constants.currentLevel = "Level_1_4"
    player.position = Object.Vector2(0, 0)

def ToWorld_2():
    Constants.currentScene = "World_2"

def ToLevel_2_1():
    Constants.currentScene = "Level_2_1"
    Constants.currentLevel = "Level_2_1"
    player.position = Object.Vector2(0, 0)

def EndLevel():
    Constants.currentScene = "World_Selection"
    Level.ResetScene(Constants.currentLevel)
    ToWorldSelection()

def QuitGame():
    Constants.gameRunning = False