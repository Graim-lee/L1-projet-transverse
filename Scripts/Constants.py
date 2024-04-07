import pygame

""" Meta informations ============================================================================================== """

# Screen dimension.
screenDimensions = (1920, 1080)
screenCenter = ((screenDimensions[0] / 2), (screenDimensions[1] / 2))

# Framerate of the game (60 FPS) and time between two frames
framerate = 60
deltaTime = 1.0 / framerate

# Whether the game is running or not.
gameRunning = True

""" Physics-related constants ====================================================================================== """

# How many times the ApplyPhysics() function (from Physics.py) will be called. The more calls, the better the precision
# but the more calculations needed.
physicsTimeDivision = 20
inverseTimeDivision = 1.0 / physicsTimeDivision

# Gravity force.
G = 25
# The force applied to an object when falling off a platform to prevent it from being floaty.
fallInitialGravity = 1500

# The maximum distance between an object and the floor for it to be considered 'grounded'.
maxGroundedDistance = 3
# A little distance to avoid the player from considering walls as floor (so that the grounded hitbox isn't exactly the
# size of the player).
groundedHitboxBorder = 0
# The friction coefficients when the player is airborne and when the player is grounded.
frictionCoeff = 1
groundedFrictionCoeff = 0.7
iceFrictionCoeff = 1
# The magnitude of the force applied to overlapping objects to manage collisions.
collisionForce = 5

""" Player controller constants ==================================================================================== """

# The horizontal speed of the player.
playerSpeed = 7000
# The maximum horizontal speed of the player.
maxPlayerSpeed = 500
# The force applied to the player when jumping, negative as y-coordinates are reversed.
playerJumpForce = -25000
# The coefficient slowing down the player when he releases the jump key ('Space') mid-air.
playerStopJumpCoeff = 0.4

# A multiplier for the slingshot propulsion force.
slingshotForce = 1.5
# The maximum force of the slingshot.
maxSlingshotForce = 650
# These three constants are used to display the trajectory of the slingshot. DO NOT CHANGE PLS I took so long to get them right :-:
slVelocityFactor = 0.33
slGravityFactor = 0.65
slGravityPower = 2.5
# This bool prevents a bug from happening, where the slingshot doesn't apply the right force (because on the first frame,
# the player is still grounded, and the game applies the ground velocity, hence reducing his speed).
playerUsedSlingshot = False
# Counts the number of jumps (= uses of slingshot) the player can perform without touching the ground. playerJumpCount is
# modified throughout the script, but maxPlayerJumpCount isn't.
#maxPlayerJumpCount is equal to 1 but in reality you can jum twice. The grounded on and 1 in the air. It represents the number of jumps in the air
maxPlayerJumpCount = 1
playerJumpCount = 1

# 1 if the player presses on D, -1 if the player presses on A/Q, 0 if the player doesn't move.
playerInputDirection = 0

# References the object the player is holding (when dealing with throwable objects).
heldItem = None
# Timer to prevent the player from picking an item instantly after throwing it (in frames).
itemThrowCooldown = 20
itemThrowTimer = 0

# Collectables

#number of coin
coin_counter = 0

"""" Camera constants ============================================================================================== """

# The x coordinates between which the player can move without moving the camera.
minXCameraMoveThreshold = 600
maxXCameraMoveThreshold = 1200
# The y coordinates.
minYCameraMoveThreshold = 400
maxYCameraMoveThreshold = 800

# The maximum distance from the camera an object can be without being unloaded.
cameraUnloadDistance = 500

""" Scene & game state constants =================================================================================== """

# Go at the end of Level.py for a list of every scene so far.

# Dictionary of the form {name_of_category: list_of_objects} containing every object to compute at a specific moment in
# the game. These objects often consist of the ones contained in the game's current scene + the objects in the 'Level_All'
# scene (the scene that is loaded everywhere).
objectsInScene: {str: []}

# The scene in which the game is currently in. 0 = MainGame (where the player can move and jump etc.); 1 = PauseMenu (the
# pause menu) ; 2 = MainMenu (the game's main menu) ; 3 = WorldSelector (where we can see each world and select the world
# we want).
currentScene = "Main_Menu"
# To remember which level the player is in even when the game is paused.
currentLevel = "Level_0"
# To have the specificity of world for the animation 1 for the ice world
currentWorld = 1
# True whenever the game is in a Menu (main menu or pause menu), False when the game is in a level.
inMenu = False

""" UI constants =================================================================================================== """

# Text fonts. The "title" font is just bigger than the "text" font.
textFont: pygame.font
titleFont: pygame.font

# Buttons constant for drawing screws.
buttonScrewSize = 8
buttonScrewDistance = 8
buttonScrewColor = (150, 150, 150)

# This variable tracks whether we pressed a button or not in the frame (prevents pressing multiple button at the same time).
buttonPressed = False

""" Animation constants ============================================================================================ """

# To keep track of whether the sprite of the player is flipped or not.
playerSpriteFlipped = False

# These variables track the actions of the player throughout the scripts to animate it properly.
playerDirection = 0
playerSquishing = False

# Constants for how many frames each sprite must stay in the animations.
playerWalkDuration = 5
playerGrounded = True
waterAnimDuration = 20

""" Skin constants ================================================================================================= """

skin = "blue"
skinList = ["blue", "black", "Iren"]
