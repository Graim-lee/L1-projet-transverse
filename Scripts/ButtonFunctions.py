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

def ToChangeSkin():
    skin_list = ["default", "black"]
    index = skin_list.index(Constants.skin)
    if index + 1 == len(skin_list):
        Constants.skin = skin_list[0]
    else:
        Constants.skin = skin_list[index + 1]

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
    player.position = Object.Vector2(0, 0)

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