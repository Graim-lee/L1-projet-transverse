import pygame
import Scripts.Object as Object
import Scripts.Constants as Constants

G = 9.81
deltaTime = Constants.deltaTime

def ApplyGravity(body: Object.GameObject):
    """ Calcule la gravité de l'objet donné et change ses coordonnées directement en fonction du résultat.
        La formule c'est Dx = 0.5 * g * (t1^2 - t0^2).
        Args:
            - object: tuple venant du pooler.
    """
    global G

    currentTime = pygame.time.get_ticks()
    previousTime = currentTime - deltaTime
    displacement = 0.5 * body.gravity * (currentTime**2 - previousTime**2)

    body.position += Object.Vector2(0, -displacement)
    body.gravity += G