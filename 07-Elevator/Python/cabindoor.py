#For Python this file uses encoding: utf-8
class CabinDoor(object):

  def __init__(self):

    #Podrían ser variables de clase... O singletons
    self.OPENED = OpenedDoorState()
    self.OPENING = OpeningDoorState()
    self.CLOSED = ClosedDoorState()
    self.CLOSING = ClosingDoorState()

    self._state = self.OPENED

  def open_button_pressed(self):
    self._state.goto_opening(self)

  def close_button_pressed(self):
    self._state.goto_closing(self)

  def closed_sensor_signal(self):
    self._state.goto_closed(self)

  def opened_sensor_signal(self):
    self._state.goto_opened(self)

  #Todo esto se podría hacer más automático, pero meh
  def is_opened(self):
    return self._state.is_opened()

  def is_closing(self):
    return self._state.is_closing()

  def is_opening(self):
    return self._state.is_opening()

  def is_closed(self):
    return self._state.is_closed()

  def go_from_opened_to_opening(self):
    pass
    #not sure
  
  def go_from_opened_to_closed(self):
    raise Exception("Can't get closed without closing first")
  
  def go_from_opened_to_opened(self):
    pass

  def go_from_opened_to_closing(self):
    self._state = self.CLOSING

  def go_from_opening_to_closed(self):
    raise Exception("Can't go from opening to closed")

  def go_from_opening_to_opened(self):
    self._state = self.OPENED

  def go_from_opening_to_closing(self):
    self._state = self.CLOSING

  def go_from_closed_to_opening(self):
    self._state = self.OPENING
  
  def go_from_closed_to_opened(self):
    raise Exception("Can't get opened without opening first")
  
  def go_from_closed_to_closing(self):
    pass
    #not sure

  def go_from_closing_to_opening(self):
    self._state = self.OPENING
  
  def go_from_closing_to_opened(self):
    raise Exception("Can't get opened by closing")
  
  def go_from_closing_to_closing(self):
    pass

  def go_from_closing_to_closed(self):
    self._state = self.CLOSED

class DoorState:
  def goto_opening(self,a_cabin_door):
    self.should_be_implemented_by_subclass()
  def goto_opened(self,a_cabin_door):
    self.should_be_implemented_by_subclass()
  def goto_closing(self,a_cabin_door):
    self.should_be_implemented_by_subclass()
  def goto_closed(self,a_cabin_door):
    self.should_be_implemented_by_subclass()
  def is_opened(self):
    return False
  def is_closed(self):
    return False
  def is_opening(self):
    return False
  def is_closing(self):
    return False
  def should_be_implemented_by_subclass():
    raise NotImplementedError("Subclass responsibility")

#Tengo dudas de que no convenga hacer todo esto con metaprogramming, pero bueno (?)
class OpenedDoorState(DoorState):
  def is_opened(self):
    return True
  def goto_opening(self,a_cabin_door):
   a_cabin_door.go_from_opened_to_opening()
  def goto_opened(self,a_cabin_door):
   a_cabin_door.go_from_opened_to_opened()
  def goto_closing(self,a_cabin_door):
   a_cabin_door.go_from_opened_to_closing()
  def goto_closed(self,a_cabin_door):
   a_cabin_door.go_from_opened_to_closed()

class ClosedDoorState(DoorState):
  def is_closed(self):
    return True
  def goto_opening(self,a_cabin_door):
   a_cabin_door.go_from_closed_to_opening()
  def goto_opened(self,a_cabin_door):
   a_cabin_door.go_from_closed_to_opened()
  def goto_closing(self,a_cabin_door):
   a_cabin_door.go_from_closed_to_closing()
  def goto_closed(self,a_cabin_door):
   a_cabin_door.go_from_closed_to_closed()

class OpeningDoorState(DoorState):
  def is_opening(self):
    return True
  def goto_opening(self,a_cabin_door):
   a_cabin_door.go_from_opening_to_opening()
  def goto_opened(self,a_cabin_door):
   a_cabin_door.go_from_opening_to_opened()
  def goto_closing(self,a_cabin_door):
   a_cabin_door.go_from_opening_to_closing()
  def goto_closed(self,a_cabin_door):
   a_cabin_door.go_from_opening_to_closed()

class ClosingDoorState(DoorState):
  def is_closing(self):
    return True
  def goto_opening(self,a_cabin_door):
   a_cabin_door.go_from_closing_to_opening()
  def goto_opened(self,a_cabin_door):
   a_cabin_door.go_from_closing_to_opened()
  def goto_closing(self,a_cabin_door):
   a_cabin_door.go_from_closing_to_closing()
  def goto_closed(self,a_cabin_door):
   a_cabin_door.go_from_closing_to_closed()
