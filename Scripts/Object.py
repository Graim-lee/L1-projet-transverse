"""
    Ce script déclare tous les types d'objets différents (classes) dans la POO.
"""
import pygame


""" ================================================================================================================ """


class GameObject:
    """ Cette classe contient toutes les infos 'récurrentes' des objets du jeu.
        - active (bool): si l'objet doit être simulé ou s'il est actuellement désactivé.
        - position (Vector2): la position (les coordonnées) de l'objet.
        - size (Vector2): la taille de l'objet (en pixels).
        - surface (Surface): la Surface de pygame (la texture) de l'objet.

        - mass (float): la masse de l'objet (0 si pas affecté par la gravité).
        - velocity (Vector2): le vecteur vitesse de l'objet.
        - gravity (float): la gravité actuelle de l'objet (utile pour calculer sa gravité à chaque frame).
        - layer (int): un nombre permettant de mettre les objets dans des catégories. Est utile pour calculer si un
                        objet devrait entrer en collision avec un autre ou non.
        - notCollidable (list[int]): liste de tous les layers avec lesquels l'objet en question ne peut pas entrer
                                        en collision (ex.: si notCollidable = [1,2], alors l'objet ne pourra pas
                                        toucher les objets de layer 1 ou 2, et passera à travers eux).
    """

    def __init__(self, _position: (int, int), _size: (int, int), _texturePath: str, _mass: float, _layer: int, _notCollidable: [int], _velocity: (int, int) = (0, 0), _active: bool = True):
        """ __init__ est appelée quand on crée l'objet.
            Args :
                - self: obligatoire pour les méthodes (fonctions d'objets).
                - _position (couple (int, int)): la position de départ de l'objet.
                - _size (couple (int, int)): la taille de l'objet.
                - _texturePath (str): le path vers la texture de l'objet.
                - _mass (float): la masse de l'objet.
                - _layer (int): le layer de l'objet.
                - _notCollidable (list[int]): liste des layers que l'objet ne pourra pas percuter (entrer en collision).
                - _velocity (couple (int, int)): la vitesse initiale de l'objet.
                - _active (bool): si l'objet est activé ou non.
        """
        self.active = _active
        self.position = Vector2(_position[0], _position[1])
        self.size = Vector2(_size[0], _size[1])
        self.surface = pygame.image.load(_texturePath).convert()
        self.Resize(_size)  # Permet d'appliquer directement la taille de l'objet.

        self.mass = _mass
        self.velocity = Vector2(_velocity[0], _velocity[1])
        self.gravity = 0
        self.layer = _layer
        self.notCollidable = _notCollidable

    def Resize(self, size: (int, int)):
        """ Permet de modifier la taille de l'objet.
            Args :
                - size (couple (int, int)): la nouvelle taille de l'objet en x et en y.
        """
        self.size = Vector2(size[0], size[1])
        self.surface = pygame.transform.scale(self.surface, size)


""" ================================================================================================================ """


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


""" ================================================================================================================ """


class Pooler:
    """ Cette classe permet de créer un pooler, c'est-à-dire un dictionnaire de la forme {nom : liste de GameObjects},
    soit {str: [GameObject]}. L'objectif du pooler est de centraliser le stockage de tous les objets pour pouvoir
    les itérer rapidement, d'avoir un stockage ordonné et de pouvoir libérer un peu de mémoire RAM (pas sûr de ça).
    J'ai fait un objet spécial pour le pooler pour pouvoir lui mettre des méthodes (= des fonctions).
        - main ({str: [GameObject]}): structure principale du pooler, un dictionnaire contenant tous les GameObjects.
    """

    def __init__(self, categories: [str]):
        """ Crée l'objet.
            Args :
                - categories ([str]): le nom de chaque catégorie d'objet présente dans le pooler (ex.: ["Player",
                                        "Wall", "Enemy"] pour séparer ces 3 types d'objets).
        """
        self.main = {}
        for name in categories:
            self.main[name] = []    # Initialise toutes les catégories comme ça {'nom_de_la_catégorie': []}.

    def AddObject(self, gameObject: GameObject, category: str):
        """ Permet d'ajouter un nouvel objet au pooler (et par extension dans le jeu).
            Args :
                - gameObject (GameObject): l'objet à ajouter au pooler.
                - category (str): la catégorie dans laquelle ajouter l'objet.
        """
        self.main[category].append(gameObject)