import pygame
import Scripts.Object as Object
import Scripts.Constants as Constants

def DrawOutline(screen: pygame.surface, position: Object.Vector2, size: Object.Vector2):
    """ Draws a black rectangular outline around the given object.
        Args:
            - screen (Surface): the screen's surface (the game window) to draw on.
            - position (Vector2): the object's position.
            - size (Vector2): the object's size.
    """
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(position.Tuple(), size.Tuple()), 5)

def DrawButtonsDots(screen: pygame.surface, position: Object.Vector2, size: Object.Vector2):
    """ Draws 4 dots in the corners of the buttons (they look like screws).
        Args:
            Same as the last function.
    """
    dotsDisplacement = [-Object.Vector2(size.x, size.y), Object.Vector2(-size.x, size.y - 2 * Constants.buttonScrewSize), Object.Vector2(size.x - 2 * Constants.buttonScrewSize, -size.y), size - 2 * Constants.buttonScrewSize * Object.Vector2(1 , 1)]
    displacementDirection = [Object.Vector2(1, 1), Object.Vector2(1, -1), Object.Vector2(-1, 1), Object.Vector2(-1, -1)]
    for i in range(4):
        drawPosition = position + 0.5 * dotsDisplacement[i] + Constants.buttonScrewDistance * displacementDirection[i]
        pygame.draw.rect(screen, Constants.buttonScrewColor, pygame.Rect(drawPosition.Tuple(), (Constants.buttonScrewSize, Constants.buttonScrewSize)))