import pygame
import Scripts.Object as Object

def DrawOutline(screen: pygame.surface, object: Object.GameObject):
    """ Draws a black rectangular outline around the given object.
        Args:
            - screen (Surface): the screen's surface (the game window) to draw on.
            - object (GameObject): the object to draw the outline around.
    """
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(object.position.Tuple(), object.size.Tuple()), 5)