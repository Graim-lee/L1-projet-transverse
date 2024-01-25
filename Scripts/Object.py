import pygame

class GameObject:
    """ Cette classe contient toutes les infos 'récurrentes' des objets du jeu.
        - position (Vector2): la position (les coordonnées) de l'objet.
        - surface (Surface): la Surface de pygame (la texture) de l'objet.
        - active (bool): si l'objet doit être simulé ou s'il est actuellement désactivé.
        - mass (float): la masse de l'objet (0 si pas affecté par la gravité).
        - gravity (float): la gravité actuelle de l'objet (utile pour calculer sa gravité à chaque frame).
    """

    def __init__(self, _position: (int, int), _texturePath: str, _mass: float, _active: bool = True):
        """ __init__ est appelée quand on crée l'objet.
            Args :
                - self: obligatoire pour les méthodes (fonctions d'objets).
                - _position (list): la position de départ de l'objet.
                - _texturePath (str): le path vers la texture de l'objet.
                - _mass (float): la masse de l'objet.
                - _active (bool): si l'objet est activé ou non.
        """
        self.position = Vector2(_position[0], _position[1])
        self.surface = pygame.image.load(_texturePath).convert()
        self.mass = _mass
        self.active = _active
        self.gravity = 0


class Vector2:
    """ Cette classe permet de stocker des coordonnées. On peut additionner des Vector2 ensemble.
        - x (int): coordonnée x (horizontale).
        - y (int): coordonnée y (verticale).
    """

    def __init__(self, _x: int, _y: int):
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

    def Tuple(self) -> (int, int):
        """ Renvoie un Tuple de la forme (a, b) car les fonctions de pygame n'acceptent pas le type Vector2.
            Args :
                - self: obligatoire.
        """
        return self.x, self.y