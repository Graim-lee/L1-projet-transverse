import pygame
import Scripts.Object as Object
import Scripts.Constants as Constants

deltaTime = Constants.deltaTime
mainPooler = Object.Pooler([])
player: Object.GameObject

def SetPooler(pooler: Object.Pooler):
    """ Allows to retrieve and copy the pooler from main.py. As the Pooler object is mutable (just like lists),
    modifying the main.py pooler will directly modify this one too. This pooler is useful for managing collisions.
        Args :
            - pooler (Pooler): the main.py pooler.
    """
    global mainPooler
    mainPooler = pooler

def SetPlayer(playerChar: Object.GameObject):
    """ Allows to retrieve and copy the player GameObject from main.py. Also mutable, so it will be shared directly
    with the main.py script. Useful for the camera position.
        Args :
            - playerChar (GameObject): the player GameObject created in main.py.
    """
    global player
    player = playerChar

def ApplyPhysics(body: Object.GameObject, i: int):
    """ Moves the object according to the PhysicsCalculations() function, called earlier in main.py. It only moves the
    object a little bit, and is called multiple times in the main loop each frame. That allows to check each frame if a
    collision is detected, and if so, cancel the movement. Thanks to that, we have more precise collision detection.
        Args :
            - body (GameObject): GameObject to move.
    """
    global mainPooler

    # In case of collision cancelling the movement, we keep track of the previous position.
    previousPosition = body.position

    # We move the object according to its velocity.
    # The formula for that movement is (x1, y1) = (x0, y0) + Dt * (Vx, Vy).
    body.position += body.velocity * deltaTime * Constants.inverseTimeDivision

    # Checking for collisions.
    for category in mainPooler.main:
        for gameObject in mainPooler.main[category]:
            if body == gameObject: continue
            if gameObject.layer in body.notCollidable: continue
            if gameObject.scene != Constants.currentScene: continue
            if not CheckCollision(body, gameObject): continue

            CancelCollision(body, gameObject)
            body.position = previousPosition
            body.collidedDuringFrame = True

def CheckCollision(body: Object.GameObject, other: Object.GameObject) -> bool:
    """ Checks if the two given GameObjects are colliding or not. It works by considering each object as 2 coordinates :
    the top-left coordinate and the bottom-right.
        Args :
            - body, other (GameObject): the two GameObjects to check.
        Returns :
            - (bool): True if the two objects are colliding, False otherwise.
    """
    topleft1, topleft2 = body.position, other.position
    bottomright1, bottomright2 = body.position + body.size, other.position + other.size

    if (bottomright1.x < topleft2.x) or (bottomright2.x < topleft1.x): return False   # If the objects are horizontally disjoint.
    if (bottomright1.y < topleft2.y) or (bottomright2.y < topleft1.y): return False     # Same but vertically.
    return True     # If the objects are neither disjoint vertically nor horizontally, they must overlap (= collision).


def CancelCollision(body: Object.GameObject, other: Object.GameObject):
    """ Activates when two objects are overlapping. Allows to stop the first object's (body) velocity towards the second
    object (other) so that he doesn't stick to it afterward.
        Args :
            - body, other (GameObject): the two objects in collision. Only body will be modified by this function.
    """
    # The average center of the collision.
    collisionCenter = GetCollisionCenter(body, other)
    # The physical center of the object (barycenter, as pygame's center is at the top-left and not in the real center).
    bodyCenter = body.position + 0.5 * body.size
    # The vector directly opposite to the collision direction.
    repelForce = bodyCenter - collisionCenter

    # We take the absolute values of the coordinates of repelForce.
    if repelForce.x < 0: repelForce.x *= -1
    if repelForce.y < 0: repelForce.y *= -1

    # We reduce the repelForce coordinates by the size of the 'body' object.
    repelForce.x *= 1.0 / body.size.x
    repelForce.y *= 1.0 / body.size.y

    # We check which axis of the repelForce is greater, and cancel it from our original velocity.
    if repelForce.x > repelForce.y:
        body.velocity.x = 0
        body.instantVelocity.x = 0
        body.continuousVelocity.x = 0
    else:
        body.velocity.y = 0
        body.instantVelocity.y = 0
        body.continuousVelocity.y = 0

def GetCollisionCenter(body: Object.GameObject, other: Object.GameObject) -> Object.Vector2:
    """ Returns the coordinates of the 'center' of the collision, that is average of every vertex concerned by the
    collision. It gives a rough estimate to where the collision really comes from.
        Args :
            - body (GameObject): the first GameObject concerned by the collision.
            - other (GameObject): the second GameObject concerned by the collision.
        Returns :
            - ((int, int)): the coordinates of the 'center' of the collision.
    """
    collisionVertices = GetCollisionVertices(body, other)   # We retrieve every vertex concerned by the collision.
    center, verticesCount = Object.Vector2(0, 0), len(collisionVertices)

    if verticesCount == 0:
        verticesCount = 1
        # The default collision center is upwards (resulting in a default downwards force).
        center = body.position + 0.5 * body.size + Object.Vector2(0, -1)

    # Same formula as for the average (the sum divided by the count).
    for vertex in collisionVertices:
        center += Object.Vector2(vertex[0], vertex[1])
    center *= 1 / float(verticesCount)

    return center

def GetCollisionVertices(body: Object.GameObject, other: Object.GameObject) -> [(int, int)]:
    """ Returns a list of tuples, representing the coordinates of each vertex concerned by the collision of the two
    objects. Useful to determine the 'center' of the collision. The algorithm works by checking if a vertex is
    in-between the top-left and the bottom-right corners of the other object.
        Args :
            - body (GameObject): the first GameObject in the collision.
            - other (GameObject): the second GameObject in the collision.
        Returns :
            - ([(int, int)]): a list of the coordinates of every vertex in the collision.
    """
    # List of all 4 vertices of the first object (in the order [top-left, bottom-right, top-right, bottom-left]).
    vertices1 = [body.position.Tuple(), (body.position + body.size).Tuple(), (body.position.x + body.size.x, body.position.y), (body.position.x, body.position.y + body.size.y)]
    # Same for the other object.
    vertices2 = [other.position.Tuple(), (other.position + other.size).Tuple(), (other.position.x + other.size.x, other.position.y), (other.position.x, other.position.y + other.size.y)]

    collisionVertices = []      # List for the return of the function.

    # Algorithm for the vertices of the first object.
    for vert1 in vertices1:
        if (vert1[0] >= vertices2[0][0]) and (vert1[1] >= vertices2[0][1]) and (vert1[0] <= vertices2[1][0]) and (vert1[1] <= vertices2[1][1]):
            collisionVertices.append(vert1)

    # Algorithm for the vertices of the second object.
    for vert2 in vertices2:
        if (vert2[0] >= vertices1[0][0]) and (vert2[1] >= vertices1[0][1]) and (vert2[0] <= vertices1[1][0]) and (vert2[1] <= vertices1[1][1]):
            collisionVertices.append(vert2)

    return collisionVertices

def MoveCamera():
    """ Used to keep the camera focused on the player. """
    displacement = player.position - Object.Vector2(Constants.screenCenter[0], Constants.screenCenter[1])

    for category in mainPooler.main:
        for gameObject in mainPooler.main[category]:
            if not gameObject.active or "Level" not in gameObject.scene: continue
            gameObject.position -= displacement

def PhysicsCalculations(body: Object.GameObject):
    """ Main function from Physics.py. Proceeds with every physics calculations.
        Args :
            - body (GameObject): GameObject to apply the physics calculations on.
    """
    # Gravity.
    grounded = CheckIfGrounded(body)
    if body.grounded and not grounded and body.velocity.y >= 0:
        body.gravity = Constants.fallInitialGravity
        body.fallingFromGround = True
        
    body.grounded = grounded
    if grounded:
        # To stop the gravity's acceleration.
        body.gravity = 0
        if body.instantVelocity.y > 0: body.instantVelocity.y = 0
        if body.continuousVelocity.y > 0: body.continuousVelocity.y = 0
    else:
        # To apply the gravity.
        ApplyGravity(body)

    ManageCollisions(body)  # Collisions.

    if not(body.fallingFromGround) and (body.instantVelocity.x > 6 or body.instantVelocity.y >6 or body.instantVelocity.x < -6 or body.instantVelocity.x < -6):
        body.velocity = body.instantVelocity
    elif not(body.fallingFromGround):
        body.velocity = body.continuousVelocity
    else:
        body.velocity = body.instantVelocity + body.continuousVelocity
    ApplyFriction(body, grounded)   # Friction.

def CheckIfGrounded(body: Object.GameObject) -> bool:
    """ Checks whether the object is grounded, that is, if it is on the floor or if it is currently falling.
        Args :
            - body (GameObject): the object we want to check.
        Returns :
            - (bool): True if the object is grounded, False otherwise.
    """
    # groundedLeft and groundedRight represent 2 points, so a segment. They are located right under the object, and
    # are used to detect if the object is grounded : if the segment overlaps with a collidable object, then the body
    # is grounded.
    groundedLeft = body.position + Object.Vector2(Constants.groundedHitboxBorder, body.size.y + Constants.maxGroundedDistance)
    groundedRight = body.position + body.size + Object.Vector2(-Constants.groundedHitboxBorder, Constants.maxGroundedDistance)

    global mainPooler
    for category in mainPooler.main:
        for gameObject in mainPooler.main[category]:
            if gameObject == body: continue
            if not gameObject.active: continue
            if gameObject.layer in body.notCollidable: continue
            if gameObject.scene != Constants.currentScene: continue

            if CheckGroundedCollision(groundedLeft, groundedRight, gameObject): 
                body.fallingFromGround = False
                return True
    return False

def CheckGroundedCollision(left: Object.Vector2, right: Object.Vector2, other: Object.GameObject) -> bool:
    """ Checks if the object's grounded hitbox collides with a given GameObject. Works similarly to CheckCollision().
        Args :
            - left, right (Vector2): the two bottom edges of the object.
            - other (GameObject): the 'floor' object to check.
        Returns :
            - (bool): True if the object is grounded, False otherwise.
    """
    topleft, bottomright = other.position, other.position + other.size

    if (left.y < topleft.y) or (left.y > bottomright.y): return False   # If the objects are vertically disjoint.
    if (right.x < topleft.x) or (left.x > bottomright.x): return False     # Same but horizontally.
    return True     # If the objects are neither disjoint vertically nor horizontally, they must overlap (= collision).

def ApplyGravity(body: Object.GameObject):
    """ Computes the object's gravity and updates its velocity vector accordingly.
    The formula is Dx = 0.5 * g * (t1^2 - t0^2).
        Args:
            - body (GameObject): GameObject for which we want to compute the gravity.
    """
    global G

    addVelocity = body.gravity * deltaTime  # The formula is given by (Vx1, Vy1) = (Vx0, Vy0) + Dt * g.

    # As pygame's coordinates system goes from top-left to bottom-right, 'downward' (the orientation of gravity)
    # is located towards increasing y coordinates, so we must add up the gravity value instead of subtracting it.
    body.instantVelocity += Object.Vector2(0, addVelocity)
    body.gravity += Constants.G

def ApplyFriction(body: Object.GameObject, grounded: bool):
    """ Slows down the body's instantVelocity and continuousVelocity by the frictionCoeff constant (see Constants.py).
    If the body is grounded, the friction coefficient is even larger, in order to slow the object down even more. Note
    that the friction only affects the horizontal velocity, as gravity already affects the vertical one.
        Args :
            - body (GameObject): the object to apply the friction to.
            - grounded (bool): whether the object is currently grounded or not.
    """
    instantHorizontal, continuousHorizontal = body.instantVelocity.x, body.continuousVelocity.x
    instantHorizontal *= Constants.frictionCoeff  # Application of the coefficients of friction.
    continuousHorizontal *= Constants.frictionCoeff  # Application of the coefficients of friction.
    if grounded and not Constants.playerUsedSlingshot:  # We do not apply the friction on the first frame of the slingshot.
        instantHorizontal *= Constants.groundedFrictionCoeff
        continuousHorizontal *= Constants.groundedFrictionCoeff

    Constants.playerUsedSlingshot = False   # To reset the 1-frame variable.

    # Completely nullifies the velocity if it is too low.
    if -0.1 <= instantHorizontal <= 0.1: instantHorizontal = 0
    if -0.1 <= continuousHorizontal <= 0.1: continuousHorizontal = 0

    body.instantVelocity.x = instantHorizontal
    body.continuousVelocity.x = continuousHorizontal

def ManageCollisions(body: Object.GameObject):
    """ Checks, computes and manages the collisions of the given object.
        Args :
            - body (GameObject): the given GameObject.
    """
    global mainPooler
    body.collisionPos = body.position
    repelForce = Object.Vector2(0, 0)   # The force applied to the object to simulate collision.
    applyForce = False                          # Stores whether to apply the repelForce or not (only apply when there is a collision).

    for category in mainPooler.main:
        for gameObject in mainPooler.main[category]:

            # I am using 'continue' everywhere to avoid spamming indentations and prevent tons of nested 'if if if'.
            # 'continue' allows to skip the current iteration of the loop, directly going to the next one.
            if gameObject == body: continue                         # When it's the same object.
            if not gameObject.active: continue                      # Deactivated objects.
            if gameObject.layer in body.notCollidable: continue     # Objects that don't collide.
            if gameObject.scene != Constants.currentScene: continue
            if not CheckCollision(body, gameObject): continue

            collisionCenter = GetCollisionCenter(body, gameObject)

            # We compute the physical center of the object (reminder : the (0 ; 0) of the object isn't at its center,
            # but rather at its top-left corner, which doesn't suit the situation).
            bodyMassCenter = body.position + 0.5 * body.size

            # We compute the orientation of the force by which we will repel the object.
            colDirection = bodyMassCenter - collisionCenter
            colDirection *= 0.1     # The smaller the vector is, the smaller the approximation error of the distance will be.

            # Knowing that its norm is a constant (see Constants.py, collisionForce), we want to normalize the vector
            # (= make it length 1) to then make it the right length.
            approxDistance = ApproxDist(colDirection.x ** 2, colDirection.y ** 2)
            normCoeff = 1 if approxDistance == 0 else (1 / approxDistance)  # To avoid any division by 0.
            colDirection *= normCoeff   # Normalized vector (length 1).
            colDirection *= Constants.collisionForce    # Vector of right length.

            # We use the collisionPos vector to update the position of the object at the end of all the physics calculations.
            repelForce += colDirection
            applyForce = True

    if applyForce:
        body.instantVelocity += repelForce  # Applying the anti-collision force.
        # We cancel the continuous velocity if the collision counters it.
        if Sign(repelForce.x) != 0 and Sign(body.continuousVelocity.x) != Sign(repelForce.x): body.continuousVelocity.x = 0
        if Sign(repelForce.y) != 0 and Sign(body.continuousVelocity.y) != Sign(repelForce.y): body.continuousVelocity.y = 0
        body.collisionDuration += Constants.deltaTime   # Keeping track of the duration of the collision.
    else:
        # Preventing the anti-collision to still affect the object after the end of the collision.
        if body.previousRepelForce.y > 0: body.instantVelocity -= body.previousRepelForce * body.collisionDuration * 0.5
        else: body.instantVelocity -= body.previousRepelForce * body.collisionDuration
        body.collisionDuration = 0

    body.previousRepelForce = repelForce

def ApproxDist(x: float, y: float) -> float:
    """ This function gives an approximation of the distance between two numbers (that is, the result of sqrt(x^2 + y^2)).
    It is useful as it takes less computational power than a regular square root, thus taking less time to run. The
    formula is : sqrt(x^2 + y^2) ~= x + (y^2 / 2x). The approximation is better for smaller x and y.
        Args :
            - x, y (float): the two numbers in the distance function.
        Returns :
            - (float): the result of the square root.
    """
    if x == 0: return y    # To avoid a division by 0.
    return x + (y ** 2) / (2 * x)

def Sign(x: float) -> int:
    """ Computes the sign of x.
        Args :
            - x (float): the number which sign we want.
        Returns :
            - (int): -1 if x is negative, 1 if x is positive, and 0 if x is null.
    """
    if x < 0: return -1
    if x > 0: return 1
    return 0