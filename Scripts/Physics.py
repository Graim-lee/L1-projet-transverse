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
    return True