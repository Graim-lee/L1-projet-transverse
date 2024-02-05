import pygame
import Scripts.InputsManager as InputsManager
import Scripts.Physics as Physics
import Scripts.Object as Object
import Scripts.Constants as Constants
import Scripts.Level as Level

""" ================================================================================================================ """
""" ==> START : put here the code that shall only run at the start of the game (i.e.: variable init., etc.). <====== """

# Creating the game's window.
screenDimensions = Constants.screenDimensions
screen = pygame.display.set_mode(screenDimensions)
screen.fill((255, 255, 255))
frame = 0

# Storing pygame's clock (to have a fixed framerate).
gameClock = pygame.time.Clock()

pooler = Level.Level0()

""" End of START =================================================================================================== """

""" ================================================================================================================ """
""" ==> UPDATE : put here the code that shall get executed each frame (i.e.: player movements, physics, etc.). <==== """

gameRunning = True

def ComputeObject(gameObject: Object.GameObject) -> bool:
    """ Returns true if the object should be rendered and applied physics on (I made a function to avoid repeating the
    enormous condition multiple times).
        Args :
            - gameObject (GameObject): the GameObject to check.
        Returns :
            - (bool): True if the object has to be rendered etc.
    """
    return gameObject.active and gameObject.visible and gameObject.scene == Constants.currentScene

def EveryObject() -> [Object.GameObject]:
    """ Returns a list of every GameObject (to avoid having to iterate through the pooler every time).
        Returns :
            - ([GameObject]): a list containing every GameObject.
    """
    result = []
    for category in pooler.main:
        for gameObject in pooler.main[category]:
            result.append(gameObject)
    return result

# Main loop of the game.
while gameRunning:

    # Retrieves and manages user inputs.
    gameRunning = InputsManager.CheckInputs()

    # Only runs when we are in the Main Game (and not in a Pause Menu or in the Main Menu).
    if "Level" in Constants.currentScene:

        # Applies the physics calculations to every object. We also reset the collidedDuringFrame variable of every
        # object to prepare it for the collision detection.
        for gameObject in EveryObject():
            if ComputeObject(gameObject) and gameObject.mass != 0:
                Physics.PhysicsCalculations(gameObject)
                gameObject.collidedDuringFrame = False

        # Updates every object's position after the calculations (updating it after every calculation is useful for
        # detecting every collision, then managing them). It is run multiple times to detect collisions more precisely
        # (see in Constants.py, physicsTimeDivision).
        for timeDiv in range(Constants.physicsTimeDivision):
            for gameObject in EveryObject():
                if ComputeObject(gameObject) and gameObject.mass != 0 and not gameObject.collidedDuringFrame:
                    Physics.ApplyPhysics(gameObject, timeDiv)

        # Camera movements. We must put that first to prevent it from glitching the physics calculations.
        Physics.MoveCamera()

        # We check that the object is still in the neighborhood of the camera. If not, we deactivate it.
        for gameObject in EveryObject():
            topLeft, bottomRight = gameObject.position, gameObject.position + gameObject.size
            if bottomRight.x < -Constants.cameraUnloadDistance or topLeft.x > Constants.cameraUnloadDistance + Constants.screenDimensions[0]:
                if not gameObject.alwaysLoaded: gameObject.visible = False
            else:
                gameObject.visible = True

        # We play the animations of the objects.
        for category in pooler.main:
            for gameObject in pooler.main[category]:
                if ComputeObject(gameObject) and gameObject.hasAnimation: gameObject.Animation(category)

    # Displays every object on the screen.
    screen.fill((255, 255, 255))    # Overwrites (erases) the last frame.

    for gameObject in EveryObject():
        if ComputeObject(gameObject):
            screen.blit(gameObject.surface, gameObject.position.Tuple())

    pygame.display.flip()   # Updates the screen's visuals.
    frame += 1

    # We wait a bit before running the next frame.
    gameClock.tick(Constants.framerate)

""" Fin de UDPATE ================================================================================================== """
