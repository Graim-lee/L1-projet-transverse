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

def ToMainMenu():
    Constants.currentScene = "Main_Menu"

def ToWorldSelection():
    Constants.currentScene = "World_Selection"

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

def EndLevel_1_2():
    Constants.currentScene = "World_1"
    Level.ResetScene("Level_1_2")

def ToLevel_1_3():
    Constants.currentScene = "Level_1_3"
    Constants.currentLevel = "Level_1_3"
    player.position = Object.Vector2(0, 0)

def ToLevel_1_4():
    Constants.currentScene = "Level_1_4"
    Constants.currentLevel = "Level_1_4"
    player.position = Object.Vector2(0, 0)

def QuitGame():
    Constants.gameRunning = False