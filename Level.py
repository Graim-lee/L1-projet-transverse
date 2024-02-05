level0 = [
platformPos = (1700, 650),
platformSize = (300, 100),

platformTexture = "Sprites/wall.png",
platformMass = 0,
platformLayer = 1,
platform = Object.GameObject(platformPos, platformSize, platformTexture, platformMass, platformLayer, [], 0),
pooler.AddObject(platform, "Wall"),]


level1 = []


fuckPos = (screenDimensions[0] / 2 - 240, 200)
fuckSize = (480, 160)
fuckTexture = "Sprites/fuck.png"
fuckMass = 0
fuckLayer = 0
fuck = Object.GameObject(fuckPos, fuckSize, fuckTexture, fuckMass, fuckLayer, [], 1, _png=True)
pooler.AddObject(fuck, "Fuck")

wall1 = (screenDimensions[0]  / 2 - 240, 900)
wallSize