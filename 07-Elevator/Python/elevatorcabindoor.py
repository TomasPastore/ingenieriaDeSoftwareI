#For Python this file uses encoding: utf-8


#^ eso es provicional... En sí se me ocurre la opción de que el ElevatorController les pase la clase... Pero no sé
#O sea, es feo porque pone una dependencia entre los archivos, cosa que no está buena :s
from elevatoremergency import ElevatorEmergency

class ElevatorCabinDoor(object):

  def __init__(self):

    #Podrían ser variables de clase... O singletons
    self.OPENING = OpeningDoorState()
    self.OPENED_AND_WAITING = OpenedAndWaitingDoorState()
    self.OPENED_AND_NOT_WAITING = OpenedAndNotWaitingDoorState()
    self.CLOSING = ClosingDoorState()
    self.CLOSED = ClosedDoorState()

    self._state = self.OPENED_AND_NOT_WAITING

  #Observadores de estado
  def is_opening(self):
    return self._state.is_opening()
  def is_opened(self):
    return self._state.is_opened()
  def is_closing(self):
    return self._state.is_closing()
  def is_closed(self):
    return self._state.is_closed()
  def is_waiting_for_people(self):
    return self._state.is_waiting_for_people()

  #Cambios de estado
  def open_button_pressed(self):
    self._state.goto_opening(self)
  def opened_sensor_signal(self):
    self._state.goto_opened_and_waiting(self)
  def close_button_pressed(self):
    self._state.goto_closing(self)
  def closed_sensor_signal(self):
    self._state.goto_closed(self)
  def wait_for_people_timed_out(self):
    self._state.goto_closing(self)

  def go_from_opening_to_opening(self):
    pass
  def go_from_opening_to_opened_and_not_waiting(self):
    raise ElevatorEmergency(ElevatorEmergency.KILLER_MACHINE)
  def go_from_opening_to_opened_and_waiting(self):
    self._state = self.OPENED_AND_WAITING
  def go_from_opening_to_closing(self):
    pass
  def go_from_opening_to_closed(self):
    raise ElevatorEmergency(ElevatorEmergency.CABIN_DOOR_SENSORS_NOT_SYNCHRONIZED)

  def go_from_opened_and_waiting_to_opening(self):
    pass  
  def go_from_opened_and_waiting_to_opened_and_waiting(self):
    pass
  def go_from_opened_and_waiting_to_opened_and_not_waiting(self):
    self._state = self.OPENED_AND_NOT_WAITING
  def go_from_opened_and_waiting_to_closing(self):
    self._state = self.CLOSING
  def go_from_opened_and_waiting_to_closed(self):
    raise ElevatorEmergency(ElevatorEmergency.CABIN_DOOR_SENSORS_NOT_SYNCHRONIZED)

  def go_from_opened_and_not_waiting_to_opening(self):
    pass
  def go_from_opened_and_not_waiting_to_opened_and_waiting(self):
    raise ElevatorEmergency(ElevatorEmergency.CABIN_DOOR_SENSORS_NOT_SYNCHRONIZED)
  def go_from_opened_and_not_waiting_to_opened_and_not_waiting(self):
    pass
  def go_from_opened_and_not_waiting_to_closing(self):
    self._state = self.CLOSING
  def go_from_opened_and_not_waiting_to_closed(self):
    raise ElevatorEmergency(ElevatorEmergency.CABIN_DOOR_SENSORS_NOT_SYNCHRONIZED)

  def go_from_closing_to_opening(self):
    self._state = self.OPENING  ##Test 7
  def go_from_closing_to_opened_and_waiting(self):
    raise ElevatorEmergency(ElevatorEmergency.CABIN_DOOR_SENSORS_NOT_SYNCHRONIZED)
  def go_from_closing_to_opened_and_not_waiting(self):
    raise ElevatorEmergency(ElevatorEmergency.CABIN_DOOR_SENSORS_NOT_SYNCHRONIZED)
  def go_from_closing_to_closing(self):
    pass
  def go_from_closing_to_closed(self):
    self._state = self.CLOSED

  def go_from_closed_to_opening(self):
    self._state = self.OPENING
  def go_from_closed_to_opened_and_waiting(self):
    raise ElevatorEmergency(ElevatorEmergency.CABIN_DOOR_SENSORS_NOT_SYNCHRONIZED)
  def go_from_closed_to_opened_and_not_waiting(self):
    raise ElevatorEmergency(ElevatorEmergency.CABIN_DOOR_SENSORS_NOT_SYNCHRONIZED)
  def go_from_closed_to_closing(self):
    pass
  def go_from_closed_to_closed(self):
  	raise ElevatorEmergency(ElevatorEmergency.CABIN_DOOR_SENSORS_NOT_SYNCHRONIZED)
  	

class DoorState:
  
  def goto_opening(self,a_cabin_door):
    self.should_be_implemented_by_subclass()
  def goto_opened_and_waiting(self,a_cabin_door):
    self.should_be_implemented_by_subclass()
  def goto_opened_and_not_waiting(self,a_cabin_door):
    self.should_be_implemented_by_subclass()
  def goto_closing(self,a_cabin_door):
    self.should_be_implemented_by_subclass()
  def goto_closed(self,a_cabin_door):
    self.should_be_implemented_by_subclass()
  def is_opening(self):
    self.should_be_implemented_by_subclass()
  def is_opened(self):
    self.should_be_implemented_by_subclass()
  def is_closing(self):
    self.should_be_implemented_by_subclass()
  def is_closed(self):
    self.should_be_implemented_by_subclass()
  def is_waiting_for_people(self):
    self.should_be_implemented_by_subclass()

  def should_be_implemented_by_subclass(self):
    raise NotImplementedError("Subclass responsibility")


class OpenedDoorState(DoorState):
  
  pass

class OpenedAndWaitingDoorState(OpenedDoorState):  
  
  def goto_opening(self,a_cabin_door):
   a_cabin_door.go_from_opened_and_waiting_to_opening()
  def goto_opened_and_waiting(self,a_cabin_door):
   a_cabin_door.go_from_opened_and_waiting_to_opened_and_waiting()
  def goto_opened_and_not_waiting(self,a_cabin_door):
   a_cabin_door.go_from_opened_and_waiting_to_opened_and_not_waiting()
  def goto_closing(self,a_cabin_door):
   a_cabin_door.go_from_opened_and_waiting_to_closing()
  def goto_closed(self,a_cabin_door):
   a_cabin_door.go_from_opened_and_waiting_to_closed()
  def is_opening(self):
    return False
  def is_opened(self):
    return True
  def is_closing(self):
    return False
  def is_closed(self):
    return False
  def is_waiting_for_people(self):
    return True

class OpenedAndNotWaitingDoorState(OpenedDoorState):

  def goto_opening(self,a_cabin_door):
   a_cabin_door.go_from_opened_and_not_waiting_to_opening()
  def goto_opened_and_waiting(self,a_cabin_door):
   a_cabin_door.go_from_opened_and_not_waiting_to_opened_and_waiting()
  def goto_opened_and_not_waiting(self,a_cabin_door):
   a_cabin_door.go_from_opened_and_not_waiting_to_opened_and_not_waiting()
  def goto_closing(self,a_cabin_door):
   a_cabin_door.go_from_opened_and_not_waiting_to_closing()
  def goto_closed(self,a_cabin_door):
   a_cabin_door.go_from_opened_and_not_waiting_to_closed()
  def is_opening(self):
    return False
  def is_opened(self):
    return True
  def is_closing(self):
    return False
  def is_closed(self):
    return False
  def is_waiting_for_people(self):
    return False

class ClosedDoorState(DoorState):
  
  def goto_opening(self,a_cabin_door):
   a_cabin_door.go_from_closed_to_opening()
  def goto_opened_and_waiting(self,a_cabin_door):
   a_cabin_door.go_from_closed_to_opened_and_waiting()
  def goto_opened_and_not_waiting(self,a_cabin_door):
   a_cabin_door.go_from_closed_to_opened_and_not_waiting()
  def goto_closing(self,a_cabin_door):
   a_cabin_door.go_from_closed_to_closing()
  def goto_closed(self,a_cabin_door):
   a_cabin_door.go_from_closed_to_closed()
  def is_opening(self):
    return False
  def is_opened(self):
    return False
  def is_closing(self):
    return False
  def is_closed(self):
    return True
def is_waiting_for_people(self):
    return False

class OpeningDoorState(DoorState):
  
  def goto_opening(self,a_cabin_door):
   a_cabin_door.go_from_opening_to_opening()
  def goto_opened_and_waiting(self,a_cabin_door):
   a_cabin_door.go_from_opening_to_opened_and_waiting()
  def goto_opened_and_not_waiting(self,a_cabin_door):
   a_cabin_door.go_from_opening_to_opened_and_not_waiting()
  def goto_closing(self,a_cabin_door):
   a_cabin_door.go_from_opening_to_closing()
  def goto_closed(self,a_cabin_door):
   a_cabin_door.go_from_opening_to_closed()
  def is_opening(self):
    return True
  def is_opened(self):
    return False
  def is_closing(self):
    return False
  def is_closed(self):
    return False
  def is_waiting_for_people(self):
    return False

class ClosingDoorState(DoorState):

  def goto_opening(self,a_cabin_door):
   a_cabin_door.go_from_closing_to_opening()
  def goto_opened_and_waiting(self,a_cabin_door):
   a_cabin_door.go_from_closing_to_opened_and_waiting()
  def goto_opened_and_not_waiting(self,a_cabin_door):
   a_cabin_door.go_from_closing_to_opened_and_not_waiting()
  def goto_closing(self,a_cabin_door):
   a_cabin_door.go_from_closing_to_closing()
  def goto_closed(self,a_cabin_door):
   a_cabin_door.go_from_closing_to_closed()
  def is_opening(self):
    return False
  def is_opened(self):
    return False
  def is_closing(self):
    return True
  def is_closed(self):
    return False
  def is_waiting_for_people(self):
    return False
