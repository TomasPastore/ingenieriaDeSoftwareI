
class ElevatorEmergency(Exception):

CABIN_SENSORS_NOT_SYNCHRONIZED = "Sensor de cabina desincronizado"
CABIN_DOOR_SENSORS_NOT_SYNCHRONIZED = "Sensor de puerta desincronizado"
KILLER_MACHINE = "El elevador quiere matar a alguien"

def __init__(self, message):
    self.message = message
