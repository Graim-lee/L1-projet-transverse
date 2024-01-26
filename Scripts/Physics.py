import pygame
import math
import Scripts.Object as Object
import Scripts.Constants as Constants

G = 0.00001
deltaTime = Constants.deltaTime
mainPooler = Object.Pooler([])

def SetPooler(pooler: {str: [Object.GameObject]}):
    """ Allows to retrieve and copy the pooler from main.py. As the Pooler object is mutable (just like lists),
    modifying the main.py pooler will directly modify this one too. This pooler is useful for managing collisions.
        Args :
            - pooler (Pooler): the main.py pooler.
    """
    global mainPooler
    mainPooler = pooler

def ApplyPhysics(body: Object.GameObject):
    """ Main function from Physics.py. Proceeds with every physics calculations and moves the objects accordingly.
        Args :
            - body (GameObject): GameObject to apply the physics calculations on.
    """
    # Gravity.
    ApplyGravity(body)

    # Collisions.
    ManageCollisions(body)

    # We move the object according to its velocity.
    # The formula for that movement is (x1, y1) = (x0, y0) + Dt * (Vx, Vy).
    body.position += body.velocity * deltaTime

def ApplyGravity(body: Object.GameObject):
    """ Computes the object's gravity and updates its velocity vector accordingly.
    The formula is Dx = 0.5 * g * (t1^2 - t0^2).
        Args:
            - body (GameObject): GameObject for which we want to compute the gravity.
    """
    global G

    currentTime = pygame.time.get_ticks()
    previousTime = currentTime - deltaTime
    addVelocity = body.gravity * deltaTime  # The formula is given by (Vx1, Vy1) = (Vx0, Vy0) + Dt * g.

    # As pygame's coordinates system goes from top-left to bottom-right, 'downward' (the orientation of gravity)
    # is located towards increasing y coordinates, so we must add up the gravity value instead of subtracting it.
    body.velocity += Object.Vector2(0, addVelocity)
    body.gravity += G

def ManageCollisions(body: Object.GameObject):
    """ Checks, computes and manages the collisions of the given object.
        Args :
            - body (GameObject): the given GameObject.
    """
    global mainPooler
    for category in mainPooler.main:
        for gameObject in mainPooler.main[category]:

            # I am using 'continue' everywhere to avoid spamming indentations and prevent tons of nested 'if if if'.
            # 'continue' allows to skip the current iteration of the loop, directly going to the next one.
            if gameObject == body: continue                         # When it's the same object.
            if not gameObject.active: continue                      # Deactivated objects.
            if gameObject.layer in body.notCollidable: continue     # Objects that don't collide.
            if not CheckCollision(body, gameObject): continue

            collisionCenter = GetCollisionCenter(body, gameObject)

            # We compute the physical center of the object (reminder : the (0 ; 0) of the object isn't at its center,
            # but rather at its top-left corner, which doesn't suit the situation).
            bodyMassCenter = body.position + 0.5 * body.size

            # We compute the orientation of the force by which we are going to repel the object apart.
            colDirection = bodyMassCenter - collisionCenter
            colDirection *= 0.1     # The smaller the vector is, the smaller the approximation error of the distance will be.

            # Knowing that its norm is a constant (see Constants.py, collisionForce), we want to normalize the vector
            # (= make it length 1) to then make it the right length.
            normCoeff = 1 / ApproxDist(colDirection.x ** 2, colDirection.y ** 2)
            colDirection *= normCoeff   # Normalized vector (length 1).
            colDirection *= Constants.collisionForce    # Vector of right length.

            # We apply the repelling force to the object's velocity.
            body.velocity += colDirection

def CheckCollision(body: Object.GameObject, other: Object.GameObject) -> bool:
    """ Checks if the two given GameObjects are colliding or not. It works by considering each object as 2 coordinates :
    the top-left coordinate and the bottom-right.
        Args :
            - body (GameObject): the first GameObject.
            - other (GameObject): the second GameObject.
        Returns :
            - (bool): True if the two objects are colliding, False otherwise.
    """
    topleft1, topleft2 = body.position, other.position
    bottomright1, bottomright2 = body.position + body.size, other.position + other.size

    if (bottomright1.x <= topleft2.x) or (bottomright2.y <= topleft1.y): return False   # If the objects are horizontally disjoint.
    if (bottomright1.y <= topleft2.y) or (bottomright2.y <= topleft1.y): return False     # Same but vertically.
    return True     # If the objects are neither disjoint vertically nor horizontally, they must overlap (= collision).

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