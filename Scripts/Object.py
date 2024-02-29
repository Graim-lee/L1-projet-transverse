"""
    This file declares every class of object for the OOP.
"""
import pygame
import Scripts.Constants as Constants


""" ================================================================================================================ """



""" ================================================================================================================ """


class GameObject:
    """ This class contain every recurrent information for objects in the game.
        - active (bool): if the object needs to appear or should not.
        - visible (bool): if the object is outside the camera's field of view, this is False and allows not to lose time
                            calculating these objects.
        - alwaysLoaded (bool): if True, prevents the object from being unloaded by the camera.
        - scene (str): the name (ID) of the scene the object is in. The scene can be named 'Level_1_1', 'Pause_Menu',
                        etc. (find the list in Constants.py), and allows not to show objects that aren't in a specific
                        scene when in another. For example, you should not be able to see the player when looking in the
                        pause menu.
        - type (str): the type of the GameObject. A 'Real' object is a rendered object in the scene, such as a wall, the
                        player or an enemy. A 'Text' object doesn't have any texture, but displays text. A 'Button' object
                        is only used in UI, it is linked to a specific function to execute when pressed.
        - data (): this parameter can take different types for every type of object. For a 'Real' GameObject, this is the
                        path of its texture in the files (it replaces texturePath).
                    For a 'Text' type GameObject, data is a tuple of the form (str, bool). The first element of the tuple
                        is the text to be displayed, and the second one is whether the text is a title or not (titles are
                        just bigger).
                    A 'Button' object takes a tuple of type (str, function). The str (first element of the tuple) is the
                        text displayed on the button. The function (second element) is the function to be executed when
                        the button is clicked.

        - position (Vector2): object's coordinates.
        - size (Vector2): object's size(in pixels).
        - surface (Surface): object's surface in pygame (texture)

        - mass (float): object's mass (0 if it should not be affected by gravity or any force).
        - velocity (Vector2): speed vector, the sum of instantVelocity and continuousVelocity. Do not directly modify
                                this vector, modify instantVelocity or continuousVelocity instead please :3
        - instantVelocity (Vector2): a Vector2 for instantaneous velocity (i.e.: explosion burst, jump force, etc.)
                                    Explanation : to distinguish from continuousVelocity, which is a velocity that
                                    should be set each frame, instantVelocity is a velocity vector that should be changed
                                    only at certain points in time (and not continuously).
        - continuousVelocity (Vector2): a Vector2 for continuous velocity. Explanation : if we just want the object to
                                        be subjected to an instantaneous force (i.e.: jumping, the force is only applied
                                        once, when the player presses 'Space'), we can add this force to the velocity
                                        vector. However, a continuous force (i.e.: the left/rightward force when moving
                                        the player, as it is applied each frame) will make the collision algorithm work.
                                        As such, this vector allows to store the continuous forces of an object for the
                                        collision algorithm to be able to cancel it if needed.
        - grounded (bool): True if the object is on the ground, False otherwise.
        - gravity (float): object's gravity (used to calculate its gravity at each frame).
        - layer (int): number to categorize objects. Useful to decide whether objects need collision or not
        - notCollidable (list[int]): list of every layers the object should not collide
                                    (i.e.: if notCollidable = [1,2], then the object will not 
                                    touch objects from layer 1 ou 2 and will go through them).

        - previousRepelForce (Vector2): stores the previous repel force exerted on the object during a collision (allows
                                    to avoid bouncing off walls and floor).
        - collisionDuration (float): stores for how long the object has been colliding with another object. Works in
                                    conjunction with previousRepelForce to prevent bouncing.
    """

    def __init__(self, _position: (int, int), _size: (int, int), _scene: str, _type: str, _data, _mass: float, _layer: int, _notCollidable: [int], _alwaysLoaded: bool = False, _png: bool = False, _hasAnimation: bool = False):
        """ __init__ is called to create an object
            Args :
                - self: mandatory for methods (objects' functions).
                - _position (tuple (int, int)): object's position.
                - _size (tuple (int, int)): object's size.
                - _scene (str): the name of the scene to which the GameObject belongs.
                - _type (str): the type of the object (a Real, a Text, or a Button...).
                - _data (): the object's data (depends on its type). See the description above.
                - _mass (float): object's mass.
                - _layer (int): objet's layer (for collisions).
                - _notCollidable (list[int]): list of layers with which the object will not collide.
                - _alwaysLoaded (bool): whether the object will always be loaded or not.
                - _png (bool): whether we want to account for transparency or not. PNG images are heavier for the game.
                - _hasAnimation (bool): whether the object has animations or not.
        """
        self.active = True
        self.visible = True
        self.alwaysLoaded = _alwaysLoaded
        self.scene = _scene

        self.position = Vector2(_position[0], _position[1])
        self.size = Vector2(_size[0], _size[1])

        # If the GameObject is of type "Real", we apply the texture.
        if _type == "Real":
            if _png: self.surface = pygame.image.load(_data)
            else: self.surface = pygame.image.load(_data).convert()
            self.Resize(_size)  # Allows to directly apply the object's new size.
        self.type = _type
        self.data = _data

        # Modifying size for 'Text' type objects.
        if _type == "Text":
            fontSize = 9 if _data[1] else 3
            self.size = fontSize * (Vector2(7, 0) * len(_data[0]) + Vector2(0, 15))

        # Modifying size for 'Button' type objects.
        if _type == "Button":
            self.size = Vector2(Constants.buttonSize[0], Constants.buttonSize[1])

        self.mass = _mass
        self.velocity = Vector2(0, 0)
        self.instantVelocity = Vector2(0, 0)
        self.continuousVelocity = Vector2(0, 0)
        self.grounded = False
        self.gravity = 0
        self.layer = _layer
        self.notCollidable = _notCollidable

        self.collidedDuringFrame = False
        self.previousRepelForce = Vector2(0, 0)
        self.collisionDuration = 0

        self.hasAnimation = _hasAnimation
        self.png = _png
        self.moving = 0
        self.previousDirection = 1
        self.spriteFlipped = False
        self.walkFrame = 0
        self.walkCycle = 0

        self.fallingFromGround = False

    def Resize(self, size: (int, int)):
        """ Modify objects size.
            Args :
                - size (couple (int, int)): New object's size on x and y.
        """
        self.size = Vector2(size[0], size[1])
        self.surface = pygame.transform.scale(self.surface, size)

    def Animation(self, category):
        """ Modify objects sprite
            Args :
                - path (string): the name of the object sprite
                - direction (list of string): [is moving, the direction]

        """
        # Idle animation.
        if self.moving == 0:
            self.SetSprite("Sprites/" + category + "/idle.png")

        # Walk animation.
        else:
            self.previousDirection = self.moving
            self.walkFrame += 1

            # Changes the animation frame.
            if self.walkFrame > 5:
                self.walkFrame = 0
                self.walkCycle += 1
                if self.walkCycle >= 2: self.walkCycle = 0
                self.SetSprite("Sprites/" + category + "/move_" + str(self.walkCycle + 1)+".png")

        # Makes the player face the right direction.
        if self.previousDirection == -1 and not self.spriteFlipped:
            self.surface = pygame.transform.flip(self.surface, True, False)
            self.spriteFlipped = True

        self.Resize((44, 44))

    def SetSprite(self, path: str):
        """ Changes the object's sprite located at the given path. Changes either by a png if the object has the _png
        tag activated or a normal image otherwise.
            Args := pygame
                - path (str): the path where the image is located.
            Returns :
                - (Surface): the pygame surface for the player.
        """
        if self.png: self.surface = pygame.image.load(path)
        else: self.surface = pygame.image.load(path).convert()
        self.spriteFlipped = False

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

    def Norm(self) -> float:
        """ Returns the norm of the vector squared. The formula is : x^2 + y^2.
            Return :
                - (float): the squared distance of the vector.
        """
        return self.x ** 2 + self.y ** 2


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

    def AddCategory(self, category: str):
        """ Let us add a new category to the pooler.
            Args :
                - category (str): the category's name.
        """
        self.main[category] = []

    def AddObject(self, gameObject: GameObject, category: str):
        """ Let us add a new object to the pooler.
            Args :
                - gameObject (GameObject): object to add in the pooler.
                - category (str): object's category.
        """
        self.main[category].append(gameObject)

    def Copy(self):
        copied = Pooler({})
        for category in self.main:
            copied.main[category] = []
            for gameObject in self.main[category]:
                copied.main[category].append(gameObject)
        return copied

    def __add__(self, other):
        """ __add__ lets us "add" two poolers. It actually just concatenates them. But with style B)
            Args :
                - self: concerned pooler.
                - other: second pooler.
        """
        result = Pooler([])

        # Concatenating elements from the first pooler.
        for category in self.main:
            result.AddCategory(category)
            for gameObject in self.main[category]:
                result.AddObject(gameObject, category)

        # Concatenating elements from the second pooler.
        for category in other.main:
            if category not in result.main: result.AddCategory(category)
            for gameObject in other.main[category]:
                result.AddObject(gameObject, category)

        return result