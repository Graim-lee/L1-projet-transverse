import pygame

class GameObject:
    """ Cette classe contient toutes les infos 'récurrentes' des objets du jeu.
        - position (Vector2): la position (les coordonnées) de l'objet.
        - surface (Surface): la Surface de pygame (la texture) de l'objet.
        - active (bool): si l'objet doit être simulé ou s'il est actuellement désactivé.
        - mass (float): la masse de l'objet (0 si pas affecté par la gravité).
        - velocity (Vector2): le vecteur vitesse de l'objet.
        - gravity (float): la gravité actuelle de l'objet (utile pour calculer sa gravité à chaque frame).
    """

    def __init__(self, _position: (int, int), _texturePath: str, _mass: float, _velocity: (int, int) = (0, 0), _active: bool = True):
        """ __init__ est appelée quand on crée l'objet.
            Args :
                - self: obligatoire pour les méthodes (fonctions d'objets).
                - _position (list): la position de départ de l'objet.
                - _texturePath (str): le path vers la texture de l'objet.
                - _mass (float): la masse de l'objet.
                - _velocity (couple (int, int)): la vitesse initiale de l'objet.
                - _active (bool): si l'objet est activé ou non.
        """
        self.position = Vector2(_position[0], _position[1])
        self.surface = pygame.image.load(_texturePath).convert()
        self.mass = _mass
        self.velocity = Vector2(_velocity[0], _velocity[1])
        self.active = _active
        self.gravity = 0


class Vector2:
    """ Cette classe permet de stocker des coordonnées. On peut additionner des Vector2 ensemble.
        - x (int): coordonnée x (horizontale).
        - y (int): coordonnée y (verticale).
    """

    def __init__(self, _x: float, _y: float):
        """ __init__ est appelée quand on crée l'objet.
            Args :
                - self: obligatoire pour les méthodes (fonctions d'objets).
                - _x (int): la coordonnée x du vecteur.
                - _y (int): la coordonnée y du vecteur.
        """
        self.x = _x
        self.y = _y

    def __add__(self, other):
        """ __add__ permet d'additionner deux vecteurs. On a (a, b) + (c, d) = (a+c, b+d).
            Args :
                - self: le premier vecteur.
                - other: le deuxième vecteur.
        """
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, other: float):
        """ __mul__ permet de multiplier un Vector2 et une float. Ca donne k * (a, b) = (ka, kb).
            Args :
                - self: le vecteur concerné.
                - other (float): le nombre par lequel on multiplie le vecteur.
        """
        return Vector2(other * self.x, other * self.y)

    def __rmul__(self, other: float):
        """ __rmul__ fait comme __mul__ mais __mul__ ne gère que le cas k * (a, b) et pas le cas (a, b) * k.
            Args :
                - self: le vecteur concerné.
                - other (float): le nombre par lequel on multiplie le vecteur.
        """
        return Vector2(other * self.x, other * self.y)

    def __repr__(self) -> str:
        """ __repr__ renvoie ce qui doit être affiché quand on print() l'objet.
            Retourne :
                - (str): ce qui sera affiché lors du print(). Ca ressemble à 'Vector2(a, b).
        """
        return "Vector2(" + str(self.x) + ", " + str(self.y) + ")"

    def Tuple(self) -> (int, int):
        """ Renvoie un Tuple de la forme (a, b) car les fonctions de pygame n'acceptent pas le type Vector2.
            Retourne :
                - (couple (int, int)): le tuple associé au vecteur.
        """
        return self.x, self.y