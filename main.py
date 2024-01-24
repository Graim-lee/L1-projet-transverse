import pygame
import Scripts.InputsManager as InputsManager

# Flemme d'expliquer mtn je vous expliquerai ça IRL.
# Chaque objet est de la forme d'un couple (rect, couleur).
pooler = {"Player": [], "Wall": []}

""" ================================================================================================================ """
""" ==> START : mettre ici tout ce qui se passe au démarrage du jeu (ex. : initialisation des variables, etc.). <=== """

# Création de la fenêtre de jeu.
screenDimensions = (1920, 1080)
screen = pygame.display.set_mode(screenDimensions)
screen.fill((255, 255, 255))

pygame.display.set_caption("Nom du jeu")    # Change le nom de la fenêtre du jeu.
pygame.display.set_icon(pygame.image.load("Sprites/game_icon.png"))     # Change l'icône du jeu.


# Création du personnage.
player = pygame.Rect(screenDimensions[0] / 2, screenDimensions[1] / 2, 10, 10)
playerColor = (0, 0, 0)
pooler["Player"].append((player, playerColor))  # On met le player dans le pooler (de la forme (rect, couleur)).

""" Fin de START =================================================================================================== """

""" ================================================================================================================ """
""" ==> UPDATE : mettre ici tout le code qui doit être éxécuté à chaque frame (ex. : mouvements du joueur, etc.). <= """

gameRunning = False

# Boucle while, mettre le code à l'intérieur svp.
while gameRunning:

    # Récupère et utilise les inputs, tout en checkant si le jeu doit s'arrêter.
    gameRunning = InputsManager.CheckInputs()


    # Affiche à l'écran tous les objets.
    for objectType in pooler:
        for poolerObject in objectType:
            pygame.draw.rect(screen, poolerObject[1], poolerObject[0])

    pygame.display.flip()   # Nécessaire pour mettre à jour les visuels.

""" Fin de UDPATE ================================================================================================== """


