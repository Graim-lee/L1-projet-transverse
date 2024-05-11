import Scripts.Object as Object

def OpenDoor(door: Object.GameObject):
    door.data = (True, door.data[1], door.data[2])