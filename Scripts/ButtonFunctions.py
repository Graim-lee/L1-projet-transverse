""" ##################################################
    Every function that will be executed when a
    button is clicked is located here.
 ################################################# """

import Scripts.Constants as Constants
import Scripts.Object as Object

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

def ToLevel_1():
    Constants.currentScene = "Level_1"
    Constants.currentLevel = "Level_1"
    player.position = Object.Vector2(0, 0)

def ToLevel_2():
    Constants.currentScene = "Level_2"
    Constants.currentLevel = "Level_2"
    player.position = Object.Vector2(0, 135)

def ToLevel_3():
    Constants.currentScene = "Level_3"
    Constants.currentLevel = "Level_3"
    player.position = Object.Vector2(0, 0)

def ToLevel_4():
    Constants.currentScene = "Level_4"
    Constants.currentLevel = "Level_4"
    player.position = Object.Vector2(0, 0)

def QuitGame():
    Constants.gameRunning = False