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

# Main loop of the game.
while gameRunning:

    # Retrieves and manages user inputs.
    gameRunning = InputsManager.CheckInputs()

    # Only runs when we are in the Main Game (and not in a Pause Menu or in the Main Menu).
    if Constants.currentScene == 0:

        # Applies the physics calculations to every object.
        for category in pooler.main:
            for gameObject in pooler.main[category]:
                if ComputeObject(gameObject) and gameObject.mass != 0:
                    Physics.PhysicsCalculations(gameObject)


        # Updates every object's position after the calculations (updating it after every calculation is useful for
        # detecting every collision, then managing them). Also reactivates / deactivates objects far enough from the camera's
        # field of view.
        for category in pooler.main:
            for gameObject in pooler.main[category]:
                if ComputeObject(gameObject) and gameObject.mass != 0:
                    Physics.ApplyPhysics(gameObject)

                    if gameObject.hasAnimation: gameObject.Animation(category)

                # We check that the object is still in the neighborhood of the camera. If not, we deactivate it.
                topLeft, bottomRight = gameObject.position, gameObject.position + gameObject.size
                if bottomRight.x < -Constants.cameraUnloadDistance or topLeft.x > Constants.cameraUnloadDistance + Constants.screenDimensions[0]:
                    if not gameObject.alwaysLoaded: gameObject.visible = False
                else:
                    gameObject.visible = True

    # Displays every object on the screen.
    screen.fill((255, 255, 255))    # Overwrites (erases) the last frame.

    for category in pooler.main:
        for gameObject in pooler.main[category]:
            if ComputeObject(gameObject):
                screen.blit(gameObject.surface, gameObject.position.Tuple())

    pygame.display.flip()   # Updates the screen's visuals.
    frame += 1

    # We wait a bit before running the next frame.
    gameClock.tick(Constants.framerate)

""" Fin de UDPATE ================================================================================================== """
