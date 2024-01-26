import pygame
import Scripts.Object as Object
import Scripts.Constants as Constants

G = 0.00001
deltaTime = Constants.deltaTime
mainPooler = Object.Pooler([])

def SetPooler(pooler: {str: [Object.GameObject]}):
    """ Permet de récupérer le pooler de main.py et de le copier. Comme l'objet Pooler est mutable (comme les listes),
    modifier le pooler de main.py modifiera directement ce pooler aussi. Le pooler est utile pour détecter des collisions.
        Args :
            - pooler (Pooler): le pooler de main.py.
    """
    global mainPooler
    mainPooler = pooler

def ApplyPhysics(body: Object.GameObject):
    """ Fonction principale de Physics.py. Réalise tous les calculs physiques et déplace l'objet en conséquence.
        Args :
            - body (GameObject): GameObject concerné.
    """
    # Gravité.
    ApplyGravity(body)

    # Collisions.
    ManageCollisions(body)

    # On déplace l'objet là où il devrait être en fonction de sa vélocité.
    # La formule c'est (x1, y1) = (x0, y0) + Dt * (Vx, Vy).
    body.position += body.velocity * deltaTime

def ApplyGravity(body: Object.GameObject):
    """ Calcule la gravité de l'objet donné et change ses coordonnées directement en fonction du résultat.
    La formule c'est Dx = 0.5 * g * (t1^2 - t0^2).
        Args:
            - body (GameObject): GameObject concerné.
    """
    global G

    currentTime = pygame.time.get_ticks()
    previousTime = currentTime - deltaTime
    addVelocity = body.gravity * deltaTime  # La formule c'est (Vx1, Vy1) = (Vx0, Vy0) + Dt * g.

    # Comme les coordonnées de pygame commencent en (0, 0) en haut à gauche de l'écran, le 'bas' (sens de la gravité)
    # se trouve vers les valeurs positives, donc on ajoute la valeur de la gravité au lieu de la soustraire.
    body.velocity += Object.Vector2(0, addVelocity)
    body.gravity += G

def ManageCollisions(body: Object.GameObject):
    """ Calcule et applique les collisions entre les différents objets.
        Args :
            - body (GameObject): le GameObject pour qui on doit vérifier les collisions.
    """
    global mainPooler
    for category in mainPooler.main:
        for gameObject in mainPooler.main[category]:
            if not gameObject.active: continue
            if CheckCollision(body, gameObject)[0] or CheckCollision(gameObject, body)[0]: return True

    return True

def CheckCollision(body: Object.GameObject, other: Object.GameObject) -> (bool, [(int, int)]):
    """ Checks if the two given GameObjects are colliding or not. It works by checking for each corner of the object.
    The function then returns every corner that are colliding with the object in order to determine where the collision
    takes place.
        Args :
            - body (GameObject): the first GameObject.
            - other (GameObject): the second GameObject.
        Returns :
            - (bool): True if the two objects are colliding, False otherwise.
            - ([(int, int)]): the list of every point that collided with the object.
    """
    x1, y1 = body.position.x, body.position.y   # Position of the first GameObject.
    a1, b1 = body.size.x, body.size.y   # Size of the first GameObject.
    x2, y2 = other.position.x, other.position.y     # Position of the second GameObject.
    a2, b2 = other.size.x, other.size.y     # Size of the second GameObject.
    points = [(x2, y2), (x2 + a2, y2), (x2, y2 + b2), (x2 + a2, y2 + b2)]   # Les quatre coins du second GameObject.

    collidedPoints = []
    for point in points:
        x, y = point[0], point[1]
        if (x > x1) and (x < x1 + a1) and (y > y1) and (y < y1 + b1): collidedPoints.append(point)
    if len(collidedPoints) > 0: return True, collidedPoints
    return False, []