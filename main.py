import pygame
import Scripts.InputsManager as InputsManager
import Scripts.Physics as Physics
import Scripts.Object as Object
import Scripts.Constants as Constants

# Flemme d'expliquer mtn je vous expliquerai ça IRL.
# N'y enregistrer que des GameObjects (voir dans Scripts/Object, la classe GameObject).
pooler = Object.Pooler(["Player", "Wall"])

""" ================================================================================================================ """
""" ==> START : mettre ici tout ce qui se passe au démarrage du jeu (ex. : initialisation des variables, etc.). <=== """

# Création de la fenêtre de jeu.
screenDimensions = (1920, 1080)
screen = pygame.display.set_mode(screenDimensions)
screen.fill((255, 255, 255))

pygame.display.set_caption("Nom du jeu")    # Change le nom de la fenêtre du jeu.
pygame.display.set_icon(pygame.image.load("Sprites/game_icon.png"))     # Change l'icône du jeu.


# On relie les poolers des différents scripts (pour qu'ils soient tous modifiés en même temps).
Physics.SetPooler(pooler)


# Création du personnage.
playerPos = (screenDimensions[0] / 2, screenDimensions[1] / 2)
playerSize = (44, 44)
playerTexture = "Sprites/player.png"
playerMass = 1
playerLayer = 0
player = Object.GameObject(playerPos, playerSize, playerTexture, playerMass, playerLayer, [])
pooler.AddObject(player, "Player")  # On met le GameObject player dans le pooler.

# Création du sol.
floorPos = (0, screenDimensions[1] - 200)
floorSize = (screenDimensions[0], 100)
floorTexture = "Sprites/wall.png"
floorMass = 0
floorLayer = 1
floor = Object.GameObject(floorPos, floorSize, floorTexture, floorMass, floorLayer, [])
pooler.AddObject(floor, "Wall")     # Paske le sol et les murs ont les mêmes propriétés, c'est un peu les mêmes objets.

""" Fin de START =================================================================================================== """

""" ================================================================================================================ """
""" ==> UPDATE : mettre ici tout le code qui doit être éxécuté à chaque frame (ex. : mouvements du joueur, etc.). <= """

gameRunning = True

# Boucle while, mettre le code à l'intérieur svp.
while gameRunning:

    # Récupère et utilise les inputs, tout en checkant si le jeu doit s'arrêter.
    gameRunning = InputsManager.CheckInputs()

    # Applique les calculs physiques à tous les objets.

    for category in pooler.main:
        for gameObject in pooler.main[category]:
            if gameObject.active and gameObject.mass != 0:
                Physics.ApplyPhysics(gameObject)

    # Affiche à l'écran tous les objets.
    screen.fill((255, 255, 255))    # Efface la frame précédente.

    for category in pooler.main:
        for gameObject in pooler.main[category]:
            if gameObject.active:
                screen.blit(gameObject.surface, gameObject.position.Tuple())

    pygame.display.flip()   # Nécessaire pour mettre à jour les visuels.


    # On laisse un peu de temps avant la prochaine frame.
    pygame.time.delay(Constants.deltaTime)

""" Fin de UDPATE ================================================================================================== """
