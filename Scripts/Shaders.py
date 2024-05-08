import pygame
import Scripts.Object as Object
import Scripts.Constants as Constants

def RenderObject(screen: pygame.surface, gameObject: Object.GameObject, category: str):
    """ Renders the given object on-screen.
        Args:
            - screen (Surface): the pygame screen's surface (the game window).
            - gameObject (GameObject): the game object to draw.
            - category (str): the category of the pooler in which the game object is contained.
    """
    # Rendering 'Real'-type and 'Door'-type objects.
    if gameObject.type == "Real" or gameObject.type == "Door" or gameObject.type == "Coin" or gameObject.type == "PressurePlate":
        screen.blit(gameObject.surface, gameObject.position.Tuple())
        # Drawing outline.
        if category == "Wall" or category == "Door":
            DrawOutline(screen, gameObject.position, gameObject.size)

    # Displaying text for 'Text' objects.
    elif gameObject.type == "Text":
        fontToUse = Constants.titleFont if gameObject.data[1] else Constants.textFont
        displayFont = fontToUse.render(gameObject.data[0], True, (0, 0, 0))
        textRect = displayFont.get_rect(center=gameObject.position.Tuple())
        screen.blit(displayFont, textRect)

    # Rendering the button and its text for 'Button' objects.
    elif gameObject.type == "Button":
        screen.blit(gameObject.surface, (gameObject.position - 0.5 * gameObject.size).Tuple())
        DrawButtonsDots(screen, gameObject.position, gameObject.size)
        displayFont = Constants.textFont.render(gameObject.data[0], True, (0, 0, 0))
        textRect = displayFont.get_rect(center=gameObject.position.Tuple())
        screen.blit(displayFont, textRect)
        DrawOutline(screen, gameObject.position - 0.5 * gameObject.size, gameObject.size)

    # Rendering the button, its text and its image for the 'WorldButton' objects.
    elif gameObject.type == "WorldButton":
        screen.blit(gameObject.surface, (gameObject.position - 0.5 * gameObject.size).Tuple())
        screen.blit(gameObject.data[2], (gameObject.position - 0.5 * gameObject.size).Tuple())
        displayFont = Constants.textFont.render(gameObject.data[0], True, (0, 0, 0))
        textRect = displayFont.get_rect(center=(gameObject.position + Object.Vector2(0, 0.6 * gameObject.size.y)).Tuple())
        screen.blit(displayFont, textRect)
        DrawOutline(screen, gameObject.position - 0.5 * gameObject.size, gameObject.size)

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