""" Meta informations ============================================================================================== """

# Screen dimension.
screenDimensions = (1920, 1080)

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
groundedHitboxBorder = 2
# The friction coefficients when the player is airborne and when the player is grounded.
frictionCoeff = 1
groundedFrictionCoeff = 0.7
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
maxPlayerJumpCount = 2
playerJumpCount = 2

# Every buffer timer (a buffer timer is a timer that allows the input of the user to be executed for a little while. For
# example, if the player presses 'Space' right before landing, the timer will let him jump just after landing).
maxJumpBufferTimer = 50

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

# The scene in which the game is currently in. 0 = MainGame (where the player can move and jump etc.); 1 = PauseMenu (the
# pause menu) ; 2 = MainMenu (the game's main menu) ; 3 = WorldSelector (where we can see each world and select the world
# we want).
currentScene = "Main_Menu"
# To remember which level the player is in even when the game is paused.
currentLevel = "Level_0"
# True whenever the game is in a Menu (main menu or pause menu), False when the game is in a level.
inMenu = False

""" UI constants =================================================================================================== """

# The size of the buttons. They all share the same size and dimensions.
buttonSize = (200, 80)
# Magical font constants to center text in a button. Do not change pls.
buttonCenterCoeff = 8.5
buttonTextHeight = 18