"""
    This file declares every classes of object for the OOP
"""
import pygame


""" ================================================================================================================ """



""" ================================================================================================================ """


class GameObject:
    """ This class contain every recurent informations for objects in the game
        - active (bool): If the object needs to appear or should not.
        - position (Vector2): object's coordinates
        - size (Vector2): objtc's size(in pixels).
        - surface (Surface): object's suface in pygame (texture)

        - mass (float): object's mass (0 if it is not affected by gravity).
        - velocity (Vector2): speed vector.
        - gravity (float): object's gravity (used to caculate its gravity at each frame).
        - layer (int): number to categorize objects. Usefull to decide whether objects need collision or not
        - notCollidable (list[int]): list of every layers the object should not collide
                                    (i.e.: if notCollidable = [1,2], then the object will not 
                                    touch objects from layer 1 ou 2 and will go through tehm).
    """

    def __init__(self, _position: (int, int), _size: (int, int), _texturePath: str, _mass: float, _layer: int, _notCollidable: [int], _velocity: (int, int) = (0, 0), _active: bool = True):
        """ __init__ is called to create an object
            Args :
                - self: mandatory for methods (objects' functions).
                - _position (tuple (int, int)): object's position.
                - _size (couple (int, int)): object's size.
                - _texturePath (str): Path for the object's texture.
                - _mass (float): object's mass.
                - _layer (int): objet's layer (for collisions).
                - _notCollidable (list[int]): list of  layers with wich the object will no collide.
                - _velocity (couple (int, int)): object's speed on x and y.
                - _active (bool): If the object should be visible or not
        """
        self.active = _active
        self.active = _active
        self.position = Vector2(_position[0], _position[1])
        self.size = Vector2(_size[0], _size[1])
        self.surface = pygame.image.load(_texturePath).convert()    # Get the texture from the path.
        self.Resize(_size)  # Allows to directly apply the object's new size.

        self.mass = _mass
        self.velocity = Vector2(_velocity[0], _velocity[1])
        self.gravity = 0
        self.layer = _layer
        self.notCollidable = _notCollidable

    def Resize(self, size: (int, int)):
        """ Modify objects size.
            Args :
                - size (couple (int, int)): New object's size on x and y.
        """
        self.size = Vector2(size[0], size[1])
        self.surface = pygame.transform.scale(self.surface, size)

    def __repr__(self) -> str:
        """ __repr__ returns what should be displayed when printing the object.
            Args :
                - self (GameObject): the concerned GameObject (mandatory).
            Returns :
                - (str): what should be displayed when printing.
        """
        return "{GameObject: size = " + str(self.size) + " | position = " + str(self.position) + "}"



""" ================================================================================================================ """


class Vector2:
    """ This class let us stock coordinates. We can add 2 vector2 between them or multiply with a scalar.
        - x (int): x coordinates (horizontal).
        - y (int): y coordinates (vertical).
    """

    def __init__(self, _x: float, _y: float):
        """ __init__ is called when creating an object.
            Args :
                - self: mandatory for methods (objects' functions).
                - _x (int): x vectors' coordinate.
                - _y (int): y vectors' coordinate.
        """
        self.x = _x
        self.y = _y

    def __add__(self, other):
        """ __add__ lets us add 2 vectors. (a, b) + (c, d) = (a+c, b+d).
            Args :
                - self: concerned vector.
                - other: second vector.
        """
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """ __sub__ lets us subtract one vector from another. (a, b) - (c, d) = (a-c, b-d).
            Args :
                - self: concerned vector.
                - other: subtracted vector.
        """
        return Vector2(self.x - other.x, self.y - other.y)

    def __rsub__(self, other):
        """ __rsub__ lets us subtract one vector from another, but the other way around (see __rmul__).
            Args :
                - self: concerned vector.
                - other: subtracted vector.
        """
        return Vector2(other.x - self.x, other.y - self.y)

    def __mul__(self, other: float):
        """ __mul__ lets us multiply a vector with a scalar(float). k * (a, b) = (ka, kb).
            Args :
                - self: concerned vector.
                - other (float): scalar used to multiply.
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
        """ __repr__ returns what should be displayed when printing the object.
            Return :
                - (str): What will be displayed with a print(). It looks like this: 'Vector2(a, b).
        """
        return "Vector2(" + str(self.x) + ", " + str(self.y) + ")"

    def Tuple(self) -> (int, int):
        """ Return a tuple of the form (a, b) because pygame's function do not accept the type vector2.
            Return :
                - (tuple (int, int)): tuple of the vector's coordinates.
        """
        return self.x, self.y


""" ================================================================================================================ """


class Pooler:
    """ this clas creates a pooler, which is a dictionary of the form {nom : liste de GameObjects} thus {str: [GameObject]}.
    The point is to centralize the stockage of every object to iterate them faster, easier to use for us and use less RAM.

    Cette classe permet de créer un pooler, c'est-à-dire un dictionnaire de la forme {nom : liste de GameObjects},
    soit {str: [GameObject]}. L'objectif du pooler est de centraliser le stockage de tous les objets pour pouvoir
    les itérer rapidement, d'avoir un stockage ordonné et de pouvoir libérer un peu de mémoire RAM (pas sûr de ça).
    J'ai fait un objet spécial pour le pooler pour pouvoir lui mettre des méthodes (= des fonctions).
        - main ({str: [GameObject]}): main structure of the pooler, a dictionary containing every GameObjects.
    """

    def __init__(self, categories: [str]):
        """ creates the object.
            Args :
                - categories ([str]): name of each category in the pooler (i.e.: ["Player", "Wall", "Enemy"] made
                                        if we want to separate categories of objects).
        """
        self.main = {}
        for name in categories:
            self.main[name] = []    # Initialise toutes les catégories comme ça {'nom_de_la_catégorie': []}.

    def AddObject(self, gameObject: GameObject, category: str):
        """ Let us add a new object to the pooler. So in the game.
            Args :
                - gameObject (GameObject): object to add in the pooler.
                - category (str): object's category.
        """
        self.main[category].append(gameObject)