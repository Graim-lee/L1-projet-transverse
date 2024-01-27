# Time between 2 frames (in milliseconds).
deltaTime = 1
# Gravity force.
G = 0.00004

# The maximum distance between an object and the floor for it to be considered 'grounded'.
maxGroundedDistance = 1
# The friction coefficients when the player is airborne and when the player is grounded.
frictionCoeff = 0.99
groundedFrictionCoeff = 0.97
# The magnitude of the force applied to overlapping objects to manage collisions.
collisionForce = 0.1


# The horizontal speed of the player.
playerSpeed = 0.1
# The maximum horizontal speed of the player.
maxPlayerSpeed = 1
# The force applied to the player when jumping, negative as y-coordinates are reversed.
playerJumpForce = -1.5
# The coefficient slowing down the player when he releases the jump key ('Space') mid-air.
playerStopJumpCoeff = 0.4

# Every buffer timer (a buffer timer is a timer that allows the input of the user to be executed for a little while. For
# example, if the player presses 'Space' right before landing, the timer will let him jump just after landing).
maxJumpBufferTimer = 50