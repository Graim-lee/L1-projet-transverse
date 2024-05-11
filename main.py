import pygame
import Scripts.InputsManager as InputsManager
import Scripts.Physics as Physics
import Scripts.Object as Object
import Scripts.Constants as Constants
import Scripts.Level as Level
import Scripts.ButtonFunctions as ButtonFunctions
import Scripts.Shaders as Shaders
import Scripts.Animations as Animations

""" ================================================================================================================ """
""" ==> START : put here the code that shall only run at the start of the game (i.e.: variable init., etc.). <====== """

# Initializing pygame.
pygame.init()

# Creating the game's window.
screenInfos = pygame.display.Info()
screenDimensions = (screenInfos.current_w, screenInfos.current_h)
Constants.screenDimensions = screenDimensions
screen = pygame.display.set_mode(screenDimensions)

# Storing pygame's clock (to have a fixed framerate).
gameClock = pygame.time.Clock()

# Initializing the text and button objects.
Constants.textFont = pygame.font.Font("Fonts/hardpixel.otf", 40)
Constants.titleFont = pygame.font.Font("Fonts/hardpixel.otf", 120)

buttonSurface = pygame.image.load("Sprites/button.png").convert()

# Initializing the backgrounds.
background = {"Main_Menu": None, "World_1": None, "World_2": None, "World_3": None}
for world in background:
    background[world] = pygame.transform.scale(pygame.image.load("Sprites/Background/" + world + ".png").convert(), screenDimensions)


# Initializing the pooler and the player.
pooler = Level.GetPooler()
Constants.objectsInScene = pooler.main["Main_Menu"]
player = pooler.main["Level_All"]["Player"][0]

# We link different objects to different scripts.
InputsManager.SetPooler(pooler)
InputsManager.SetPlayer(player)
Physics.SetPlayer(player)
ButtonFunctions.SetPlayer(player)


""" End of START =================================================================================================== """

""" ================================================================================================================ """
""" ==> UPDATE : put here the code that shall get executed each frame (i.e.: player movements, physics, etc.). <==== """

def ComputeObject(gameObject: Object.GameObject) -> bool:
    """ Returns true if the object should be rendered and applied physics on (I made a function to avoid repeating the
    enormous condition multiple times).
        Args :
            - gameObject (GameObject): the GameObject to check.
        Returns :
            - (bool): True if the object has to be rendered etc.
    """
    return gameObject.active and gameObject.visible

# Main loop of the game.
while Constants.gameRunning:
    # Manages user inputs.
    InputsManager.CheckInputs()


    # We retrieve every object and category that we want to access during the frame.
    concatScene = [Constants.currentScene] if Constants.inMenu else [Constants.currentScene, "Level_All"]
    Constants.objectsInScene = pooler.SceneConcat(concatScene)

    # Only runs when we are in the Main Game (and not in a Pause Menu or in the Main Menu).
    if not Constants.inMenu:

        # Applies the physics calculations to every object. We also reset the collidedDuringFrame variable of every
        # object to prepare it for the collision detection. Moreover we apply velocity when needed for the background object.
        for category in Constants.objectsInScene:
            for gameObject in Constants.objectsInScene[category]:
                Physics.VelocityBackgroundObject(category, gameObject)
                if ComputeObject(gameObject) and gameObject.mass != 0:
                    Physics.PhysicsCalculations(gameObject)
                    gameObject.collidedDuringFrame = False
                    

        # Updates every object's position after the calculations (updating it after every calculation is useful for
        # detecting every collision, then managing them). It is run multiple times to detect collisions more precisely
        # (see in Constants.py, physicsTimeDivision). 
        for timeDiv in range(Constants.physicsTimeDivision):
            for category in Constants.objectsInScene:
                for gameObject in Constants.objectsInScene[category]:
                    Physics.ApplyVelocityBackgroundObject(category, gameObject)
                    if ComputeObject(gameObject) and gameObject.mass != 0 and not gameObject.collidedDuringFrame:   
                        if gameObject.touchingPlatform:
                            Physics.TouchingPlatform(gameObject, gameObject.touchingPlatform)
                            Physics.MovingBodyWithPlatform(gameObject, gameObject.touchingPlatform)
                        elif gameObject.onPlatform:
                            Physics.MovingBodyWithPlatform(gameObject, gameObject.onPlatform)
                        Physics.ApplyPhysics(gameObject, timeDiv)

        # We move the player after calculating the collisions etc.
        InputsManager.MovePlayer(Constants.playerInputDirection)
        # We update the pressure plates and the mechanical doors.
        Physics.UpdatePressurePlates()
        Physics.UpdateMechanicalDoors()
        # Camera movements. We must put that first to prevent it from glitching the physics calculations.
        Physics.MoveCamera()

        # We check that the object is still in the neighborhood of the camera. If not, we deactivate it.
        for category in Constants.objectsInScene:
            for gameObject in Constants.objectsInScene[category]:
                topLeft, bottomRight = gameObject.position, gameObject.position + gameObject.size
                if bottomRight.x < -Constants.cameraUnloadDistance or topLeft.x > Constants.cameraUnloadDistance + Constants.screenDimensions[0]:
                    if not gameObject.alwaysLoaded: gameObject.visible = False
                else:
                    gameObject.visible = True

        # We play the animations of the objects.
        for category in Constants.objectsInScene:
            if category == "Water": Animations.AnimateWater(Constants.objectsInScene[category])
            if category == "Player": Animations.AnimatePlayer(Constants.objectsInScene[category][0])
            if category == "Coin": Animations.AnimateCoin(Constants.objectsInScene[category])

    # Displays every object on the screen (two loops for objects in the scene and objects in "Level_All").
    screen.blit(background[Constants.currentWorld], (0, 0))    # Overwrites (erases) the last frame.

    for category in Constants.objectsInScene:
        for gameObject in Constants.objectsInScene[category]:
            if ComputeObject(gameObject):
                Shaders.RenderObject(screen, gameObject, category)

    pygame.display.flip()   # Updates the screen's visuals.

    # We wait a bit before running the next frame.
    gameClock.tick(Constants.framerate)

""" Fin de UDPATE ================================================================================================== """
