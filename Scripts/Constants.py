# Screen dimension.
screenDimensions = (1920, 1080)

# Time between 2 frames (in milliseconds).
deltaTime = 1
# Gravity force.
G = 0.00006
# The force applied to an object when falling off a platform to prevent it from being floaty.
fallInitialGravity = 0.018

# The maximum distance between an object and the floor for it to be considered 'grounded'.
maxGroundedDistance = 1
# A little distance to avoid the player from considering walls as floor (so that the grounded hitbox isn't exactly the
# size of the player).
groundedHitboxBorder = 2
# The friction coefficients when the player is airborne and when the player is grounded.
frictionCoeff = 1
groundedFrictionCoeff = 0.95
# The magnitude of the force applied to overlapping objects to manage collisions.
collisionForce = 0.5


# The horizontal speed of the player.
playerSpeed = 0.5
# The maximum horizontal speed of the player.
maxPlayerSpeed = 1
# The force applied to the player when jumping, negative as y-coordinates are reversed.
playerJumpForce = -1.5
# The coefficient slowing down the player when he releases the jump key ('Space') mid-air.
playerStopJumpCoeff = 0.4


# The x coordinates between which the player can move without moving the camera.
minXCameraMoveThreshold = 600
maxXCameraMoveThreshold = 1200
# The y coordinates
minYCameraMoveThreshold = 400 #if is increase will make the camera lower when we go to high
maxYCameraMoveThreshold = 800

# The maximum distance from the camera an object can be without being unloaded.
cameraUnloadDistance = 500

# Every buffer timer (a buffer timer is a timer that allows the input of the user to be executed for a little while. For
# example, if the player presses 'Space' right before landing, the timer will let him jump just after landing).
maxJumpBufferTimer = 50


# The scene in which the game is currently in. 0 = MainGame (where the player can move and jump etc.); 1 = PauseMenu (the
# pause menu) ; 2 = MainMenu (the game's main menu) ; 3 = WorldSelector (where we can see each world and select the world
# we want).
currentScene = 0