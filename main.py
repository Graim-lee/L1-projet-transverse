import pygame
import Scripts.InputsManager as InputsManager
import Scripts.Physics as Physics
import Scripts.Object as Object
import Scripts.Constants as Constants

# Pooler object from the Object.py script. See there to get a description.
pooler = Object.Pooler(["Player", "Wall"])

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
player = Object.GameObject(playerPos, playerSize, playerTexture, playerMass, playerLayer, [])
pooler.AddObject(player, "Player")  # On met le GameObject player dans le pooler.

# Creating the test floor.
floorPos = (0, screenDimensions[1]- 200)
floorSize = (screenDimensions[0]*5, 100)
floorTexture = "Sprites/floar.png"
floorMass = 0
floorLayer = 1
floor = Object.GameObject(floorPos, floorSize, floorTexture, floorMass, floorLayer, [])
pooler.AddObject(floor, "Wall")     # We put the floor in the 'Wall' category as they share the same properties.


# Creating the left wall.
wallPos = (-600, 0)
wallSize = (600, screenDimensions[1])
wallTexture = "Sprites/wall.png"
wallMass = 0
wallLayer = 1
wall = Object.GameObject(wallPos, wallSize, wallTexture, wallMass, wallLayer, [])
pooler.AddObject(wall, "Wall")

platformPos = (1700, 750)
platformSize = (100, 25)
platformTexture = "Sprites/wall.png"
platformMass = 0
platformLayer = 1
platform = Object.GameObject(platformPos, platformSize, platformTexture, platformMass, platformLayer, [])
pooler.AddObject(platform, "Wall")

# We link different objects to different scripts.
InputsManager.SetPooler(pooler)
InputsManager.SetPlayer(player)
Physics.SetPooler(pooler)
Physics.SetPlayer(player)

""" End of START =================================================================================================== """

""" ================================================================================================================ """
""" ==> UPDATE : put here the code that shall get executed each frame (i.e.: player movements, physics, etc.). <==== """

gameRunning = True

# Main loop of the game.
while gameRunning:

    # Retrieves and manages user inputs.
    gameRunning = InputsManager.CheckInputs()
    # Applies the physics calculations to every object.
    for category in pooler.main:
        for gameObject in pooler.main[category]:
            if gameObject.active and gameObject.mass != 0:
                Physics.PhysicsCalculations(gameObject)


    # Updates every object's position after the calculations (updating it after every calculation is useful for
    # detecting every collision, then managing them).
    for category in pooler.main:
        for gameObject in pooler.main[category]:
            if gameObject.active and gameObject.mass != 0:
                Physics.ApplyPhysics(gameObject)

    # Display every object on the screen.
    # Display every object on the screen.
    screen.fill((255, 255, 255))    # Overwrites (erases) the last frame.

    for category in pooler.main:
        for gameObject in pooler.main[category]:
            if gameObject.active:
                screen.blit(gameObject.surface, gameObject.position.Tuple())

    pygame.display.flip()   # Updates the screen's visuals.


    # We wait a bit before running the next frame.
    pygame.time.delay(Constants.deltaTime)

""" Fin de UDPATE ================================================================================================== """
