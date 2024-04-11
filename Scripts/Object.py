
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
        - type (str): the type of the GameObject. A 'Real' object is a rendered object in the scene, such as a wall, the
                        player or an enemy. A 'Door' object is like a 'Real' object, but it has a function associated to
                        it that activates when the player interacts with the door. A 'Text' object doesn't have any
                        texture, but displays text. A 'Button' object
                        is only used in UI, it is linked to a specific function to execute when pressed. A 'WorldButton'
                        object is like a 'Button' object, but with an image inside.
        - data (): this parameter can take different types for every type of object. For a 'Real' GameObject, this is the
                        path of its texture in the files (it replaces texturePath).
                    For a 'Door' object, it is a tuple of the form (str, function), where the first string is the path to
                        the door's texture, and the function is the function that should be executed when interacting with
                        the door.
                    For a 'Text' type GameObject, data is a tuple of the form (str, bool). The first element of the tuple
                        is the text to be displayed, and the second one is whether the text is a title or not (titles are
                        just bigger).
                    A 'Button' object takes a tuple of type (str, function). The str (first element of the tuple) is the
                        text displayed on the button. The function (second element) is the function to be executed when
                        the button is clicked.
                    A 'WorldButton' object takes a tuple of type (str, function, str). The first two are the same as a
                        'Button' object, and the last str is the path to the image inside the button.

        - position (Vector2): object's current coordinates.
        - initialPosition (Vector2): object's coordinates at the start of the game (used to reset levels).
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
                                    touch objects from layer 1 are 2 and will go through them).
        - slippery (bool): True if the object has ice-like properties (that is, objects slide on top of it).
        - onIce (bool): True if the object is currently on ice (and is subject to the ice effects such as sliding etc.)

        - previousRepelForce (Vector2): stores the previous repel force exerted on the object during a collision (allows
                                    to avoid bouncing off walls and floor).
        - collisionDuration (float): stores for how long the object has been colliding with another object. Works in
                                    conjunction with previousRepelForce to prevent bouncing.
    """

    def __init__(self, _position: (int, int), _size: (int, int), _type: str, _data, _mass: float, _layer: int, _notCollidable: [int], _alwaysLoaded: bool = False, _png: bool = False, _hasAnimation: bool = False, _slippery = False):
        """ __init__ is called to create an object
            Args :
                - self: mandatory for methods (objects' functions).
                - _position (tuple (int, int)): object's position.
                - _size (tuple (int, int)): object's size.
                - _type (str): the type of the object (a Real, a Text, or a Button...).
                - _data (): the object's data (depends on its type). See the description above.
                - _mass (float): object's mass.
                - _layer (int): objet's layer (for collisions).
                - _notCollidable (list[int]): list of layers with which the object will not collide.
                - _alwaysLoaded (bool): whether the object will always be loaded or not.
                - _png (bool): whether we want to account for transparency or not. PNG images are heavier for the game.
                - _hasAnimation (bool): whether the object has animations or not.
                - _slippery (bool): whether the object has ice properties (players slides and can only jump).
        """
        self.active = True
        self.visible = True
        self.alwaysLoaded = _alwaysLoaded

        self.position = Vector2(_position[0], _position[1])
        self.initialPosition = Vector2(_position[0], _position[1])
        self.size = Vector2(_size[0], _size[1])

        # We fetch the object's texture if needed.
        if _type == "Real" or _type == "Coin" :
            if _png: self.surface = pygame.image.load(_data)
            else: self.surface = pygame.image.load(_data).convert()
        elif _type == "Door":
            self.surface = pygame.image.load(_data[0]).convert()
        elif _type == "Button" or _type == "WorldButton":
            self.surface = pygame.image.load("Sprites/button.png").convert()

        # We modify the size of the "Real" and "Button" game objects.
        if _type == "Real" or _type == "Door" or _type == "Button" or _type == "Coin":
            self.Resize(_size)  # Allows to directly apply the object's new size.

        self.type = _type
        self.data = _data

        if _type == "WorldButton":
            worldSurface = pygame.image.load(_data[2]).convert()
            worldSurface = pygame.transform.scale(worldSurface, _size)
            self.data = (_data[0], _data[1], worldSurface)

        self.mass = _mass
        self.velocity = Vector2(0, 0)
        self.grounded = False
        self.gravity = 0
        self.layer = _layer
        self.notCollidable = _notCollidable

        self.collidedDuringFrame = False
        self.previousRepelForce = Vector2(0, 0)
        self.collisionDuration = 0

        self.hasAnimation = _hasAnimation
        self.png = _png

        self.fallingFromGround = False
        self.slippery = _slippery
        self.onIce = False
        self.OnPlatform = False

    def Resize(self, size: (int, int)):
        """ Modify objects size.
            Args :
                - size (couple (int, int)): New object's size on x and y.
        """
        self.size = Vector2(size[0], size[1])
        self.surface = pygame.transform.scale(self.surface, size)

    def SetSprite(self, path: str, isPlayer: bool):
        """ Changes the object's sprite located at the given path. Changes either by a png if the object has the _png
        tag activated or a normal image otherwise.
            Args := pygame
                - path (str): the path where the image is located.
                - isPlayer (bool): must be set to true when the object is the player. Allows for correct player animations.
            Returns :
                - (Surface): the pygame surface for the player.
        """
        if self.png: self.surface = pygame.image.load(path)
        else: self.surface = pygame.image.load(path).convert()
        if isPlayer:
            self.surface = pygame.transform.flip(self.surface, True, False)
            Constants.playerSpriteFlipped = True
        else: Constants.playerSpriteFlipped = False

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
        """ __rmul__ makes like __mul__ but __mul__ only manages the case k * (a, b) and not (a, b) * k.
            Args :
                - self: concerned vector.
                - other (float): the coefficient by which we multiply the vector.
        """
        return Vector2(other * self.x, other * self.y)

    def __repr__(self) -> str:
        """ __repr__ returns what should be displayed when printing the object.
            Return :
                - (str): What will be displayed with a print(). It looks like this: 'Vector2(a, b).
        """
        return "Vector2(" + str(self.x) + ", " + str(self.y) + ")"

    def __neg__(self):
        """ __neg__ returns what the 'negative' of a Vector2 should be. -(a ; b) = (-a ; -b)
            Args :
                - self: concerned vector.
        """
        return Vector2(-self.x, -self.y)

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
    """ This class creates a pooler, which is a dictionary of dictionary of the form:
     {name_of_level: {name_of_category: list_of_objects} } thus {str: {str: [GameObject]}}.
    The point is to centralize the storage of every object to iterate them faster, easier to use for us and use less RAM.
    We made a custom object specifically for this to use methods (= functions) specific to it.
        - main ({str: {str: [GameObject]}}): main structure of the pooler, a dictionary where keys are level names, and
                                            values are dictionaries of the form {name_of_the_category: list_of_objects}.
    """

    def __init__(self):
        """ Creates an empty pooler. """
        self.main = {}

    def SetScene(self, scene: str, objects: {str: GameObject}):
        """ Will fill the dictionary of the specified scene in the pooler using the 'objects' dictionary. We do it object
        by object to avoid linking the lists (we want the scene to be a copy of the original 'objects' dictionary).
            Args:
                - scene (str): the name of the scene to fill.
                - objects ({str: GameObject}): the dictionary used to fill the scene. Of the form {name_of_category: list_of_objects}.
        """
        self.main[scene] = {}
        for category in objects:
            self.main[scene][category] = []
            for gameObject in objects[category]:
                self.main[scene][category].append(gameObject)

    def GetCategoriesIn(self, scene: str) -> [str]:
        """ Returns the list of every category contained in the given scene OR in the 'Level_All' scene.
            Args:
                - scene (str): the scene to retrieve the categories from.
            Returns:
                - ([str]): a list containing the names of every category.
        """
        result = []
        for category in self.main[scene]: result.append(category)
        for category in self.main["Level_All"]:
            if category not in result: result.append(category)
        return result

    def GetObjectsIn(self, scene: str, category: str) -> [GameObject]:
        """ Returns a list of every object contained in the specific category of the given level OR the 'Level_All' scene.
            Args:
                - scene (str): the scene to retrieve the objects from.
                - category (str): the category to retrieve the objects from.
            Returns:
                - ([GameObject]): the game objects to retrieve.
        """
        result = []
        for gameObject in self.main[scene][category]: result.append(gameObject)
        for gameObject in self.main["Level_All"][category]:
            if gameObject not in result: result.append(gameObject)
        return result

    def SceneConcat(self, scenes: [str]) -> {str: [GameObject]}:
        """ Returns a concatenated version of every scene given, that is, a dictionary of the form
        {name_of_category : list_of_gameobjects} containing each category and game object of every scene given in the
        'scenes' list.
            Args:
                - scenes ([str]): list of every scene to be concatenated.
        """
        result = {}
        for scene in scenes:
            for category in self.main[scene]:
                if category not in result: result[category] = []
                for gameObject in self.main[scene][category]:
                    result[category].append(gameObject)
        return result

    def Copy(self):
        copied = Pooler()
        for scene in self.main:
            copied.main[scene] = {}
            for category in self.main[scene]:
                copied.main[category] = []
                for gameObject in self.main[scene][category]:
                    copied.main[scene][category].append(gameObject)
        return copied

    def __add__(self, other):
        """ __add__ lets us "add" two poolers. It actually just concatenates them. But with style B)
            Args :
                - self: concerned pooler.
                - other: second pooler.
        """
        result = Pooler()

        # Concatenating elements from the first pooler.
        for scene in self.main:
            result.main[scene] = {}
            for category in self.main[scene]:
                result.main[scene][category] = []
                for gameObject in self.main[scene][category]:
                    result.main[scene][category].append(gameObject)

        # Concatenating elements from the second pooler.
        for scene in other.main:
            if scene not in result.main: result.main[scene] = {}
            for category in other.main[scene]:
                if category not in result.main[scene]: result.main[scene][category] = []
                for gameObject in other.main[category]:
                    result.main[scene][category].append(gameObject)

        return result