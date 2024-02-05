import pygame
import Scripts.InputsManager as InputsManager
import Scripts.Physics as Physics
import Scripts.Object as Object
import Scripts.Constants as Constants

# Pooler object from the Object.py script. See there to get a description.
pooler = Object.Pooler(["Player", "Wall", "Fuck"])

""" ================================================================================================================ """
""" ==> START : put here the code that shall only run at the start of the game (i.e.: variable init., etc.). <====== """

# Creating the game's window.
screenDimensions = (1920, 1080)
screen = pygame.display.set_mode(screenDimensions)
screen.fill((255, 255, 255))

pygame.display.set_caption("Nom du jeu")    # Changes the name of the game's window.
pygame.display.set_icon(pygame.image.load("Sprites/game_icon.png"))     # Changes the icon of the game's window.

# Creating the player's character.
playerPos = (screenDimensions[0] / 2, 700)
playerSize = (44, 44)
playerTexture = "Sprites/player.png"
playerMass = 1
playerLayer = 0
player = Object.GameObject(playerPos, playerSize, playerTexture, playerMass, playerLayer, [], 0, True, True, True)
pooler.AddObject(player, "Player")  # On met le GameObject player dans le pooler.

# Creating the test floor.
floorPos = (0, screenDimensions[1] - 200)
floorSize = (screenDimensions[0]*5, 100)
floorTexture = "Sprites/floar.png"
floorMass = 0
floorLayer = 1
floor = Object.GameObject(floorPos, floorSize, floorTexture, floorMass, floorLayer, [], 0)
pooler.AddObject(floor, "Wall")     # We put the floor in the 'Wall' category as they share the same properties.


# Creating the left wall.
wallPos = (-600, 0)
wallSize = (600, screenDimensions[1])
wallTexture = "Sprites/wall.png"
wallMass = 0
wallLayer = 1
wall = Object.GameObject(wallPos, wallSize, wallTexture, wallMass, wallLayer, [], 0)
pooler.AddObject(wall, "Wall")


platformPos = (1700, 650)
platformSize = (300, 100)

platformTexture = "Sprites/wall.png"
platformMass = 0
platformLayer = 1
platform = Object.GameObject(platformPos, platformSize, platformTexture, platformMass, platformLayer, [], 0)
pooler.AddObject(platform, "Wall")

fuckPos = (screenDimensions[0] / 2 - 240, 200)
fuckSize = (480, 160)
fuckTexture = "Sprites/fuck.png"
fuckMass = 0
fuckLayer = 0
fuck = Object.GameObject(fuckPos, fuckSize, fuckTexture, fuckMass, fuckLayer, [], 1, _png=True)
pooler.AddObject(fuck, "Fuck")

# We link different objects to different scripts.
InputsManager.SetPooler(pooler)
InputsManager.SetPlayer(player)
Physics.SetPooler(pooler)
Physics.SetPlayer(player)

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
    gameRunning, direction = InputsManager.CheckInputs()

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
                    AnimationCoolDown = 75
                    if pygame.time.get_ticks() % AnimationCoolDown == 0:
                        gameObject.Animation(category, direction)

                # We check that the object is still in the neighborhood of the camera. If not, we deactivate it.
                topLeft, bottomRight = gameObject.position, gameObject.position + gameObject.size
                if bottomRight.x < -Constants.cameraUnloadDistance or topLeft.x > Constants.cameraUnloadDistance + screenDimensions[0]:
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


    # We wait a bit before running the next frame.
    pygame.time.delay(Constants.deltaTime)

""" Fin de UDPATE ================================================================================================== """
