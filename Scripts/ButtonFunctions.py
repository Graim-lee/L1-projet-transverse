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

def ToWorldSelection():
    Constants.currentScene = "World_Selection"


def ToLevel_0():
    Constants.currentScene = "Level_0"
    Constants.currentLevel = "Level_0"
    player.position = Object.Vector2(Constants.screenDimensions[0] / 2, 500)

def ToLevel_1():
    Constants.currentScene = "Level_1"
    Constants.currentLevel = "Level_1"
    player.position = Object.Vector2(Constants.screenDimensions[0] / 2, 500)

def ToLevel_2():
    Constants.currentScene = "Level_2"
    Constants.currentLevel = "Level_2"
    player.position = Object.Vector2(Constants.screenDimensions[0] / 2 - 20, 700) # position player

def QuitGame():
    Constants.gameRunning = False