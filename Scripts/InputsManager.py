""" InputsManager.py
    Gère les inputs.
"""
import pygame

def CheckInputs() -> bool:
    """ Fonction principale, regarde tous les inputs. Si vous voulez détecter une touche, mettre le code ici.
        Retourne:
            - bool : True si le jeu continue à tourner, False si le jeu doit s'arrêter.
    """

    # Tous les inputs utilisés.
    for event in pygame.event.get():

        # KEYDOWN = l'utilisateur a appuyé sur une touche.
        if event.type == pygame.KEYDOWN:

            # 'Escape' = fin du jeu.
            if event.key == pygame.K_ESCAPE:
                return False

    return True