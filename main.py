import pygame
import Scripts.InputsManager as InputsManager
import Scripts.Physics as Physics
import Scripts.Object as Object
import Scripts.Constants as Constants

# Flemme d'expliquer mtn je vous expliquerai ça IRL.
# N'y enregistrer que des GameObjects (voir dans Scripts/Object, la classe GameObject).
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
playerPos = (screenDimensions[0] / 2, screenDimensions[1] / 2)
playerTexture = "Sprites/player.png"
playerMass = 1
player = Object.GameObject(playerPos, playerTexture, playerMass)
pooler["Player"].append(player)  # On met le GameObject player dans le pooler.

# Création du sol.
floorPos = (0, screenDimensions[1] - 200)
floorTexture = "Sprites/wall.png"
floorGravity = 0
floor = Object.GameObject(floorPos, floorTexture, floorGravity)
pooler["Wall"].append(floor)

""" Fin de START =================================================================================================== """

""" ================================================================================================================ """
""" ==> UPDATE : mettre ici tout le code qui doit être éxécuté à chaque frame (ex. : mouvements du joueur, etc.). <= """

gameRunning = True

# Boucle while, mettre le code à l'intérieur svp.
while gameRunning:

    # Récupère et utilise les inputs, tout en checkant si le jeu doit s'arrêter.
    gameRunning = InputsManager.CheckInputs()

    # Applique les calculs physiques à tous les objets.
    for objectType in pooler:
        for gameObject in pooler[objectType]:
            if gameObject.mass != 0:
                Physics.ApplyPhysics(gameObject)

    # Affiche à l'écran tous les objets.
    screen.fill((255, 255, 255))    # Efface la frame précédente.

    for objectType in pooler:
        for gameObject in pooler[objectType]:
            screen.blit(gameObject.surface, gameObject.position.Tuple())

    pygame.display.flip()   # Nécessaire pour mettre à jour les visuels.


    # On laisse un peu de temps avant la prochaine frame.
    pygame.time.delay(Constants.deltaTime)

""" Fin de UDPATE ================================================================================================== """

