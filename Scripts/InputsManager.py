""" InputsManager.py
    Manage inputs
"""
import pygame

def CheckInputs() -> bool:
    """ Main function, check every inputs. Si vous voulez détecter une touche, mettre le code ici.
        return:
            - bool : True if the game is running, False in the contrary
    """

    # Evry inputs
    for event in pygame.event.get():

        # KEYDOWN = the user pushed a key.
        if event.type == pygame.KEYDOWN:

            # 'Escape' = end of the game.
            if event.key == pygame.K_ESCAPE:
                return False

    return True