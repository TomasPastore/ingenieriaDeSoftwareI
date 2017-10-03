class CabinDoor(object):

  def __init__(self):

    self.OPENED = OpenedDoorState()
    self.OPENING = OpeningDoorState()
    self.CLOSED = ClosedDoorState()
    self.CLOSING = ClosingDoorState()

    self._state = self.OPENED

  def open_button_pressed(self):
    self._state.goto_opening(self)

  def close_button_pressed(self):
    self._state.goto_closening(self)

  def closed_sensor_signal(self):
    self._state.goto_closed(self)

  def opened_sensor_signal(self):
    self._state.goto_opened(self)

  def go_from_opened_to_opening(self):
    pass
    #not sure
  
  def go_from_opened_to_opened(self):
    raise Exception("Can't get closed without closing first")
  
  def go_from_opened_to_closing(self):
    self._state = CLOSING

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

class DoorState:
  def goto_opening(self,a_cabin_door):
    self.should_be_implemented_by_subclass()
  def goto_opened(self,a_cabin_door):
    self.should_be_implemented_by_subclass()
  def goto_closing(self,a_cabin_door):
    self.should_be_implemented_by_subclass()
  def goto_closed(self,a_cabin_door):
    self.should_be_implemented_by_subclass()
  def should_be_implemented_by_subclass():
    raise NotImplementedError("Subclass responsibility")

#Tengo dudas de que no convenga hacer todo esto con metaprogramming, pero bueno (?)
class OpenedDoorState(DoorState):
  def goto_opening(self,a_cabin_door):
   a_cabin_door.go_from_opened_to_opening()
  def goto_opened(self,a_cabin_door):
   a_cabin_door.go_from_opened_to_opened()
  def goto_closing(self,a_cabin_door):
   a_cabin_door.go_from_opened_to_closing()
  def goto_closed(self,a_cabin_door):
   a_cabin_door.go_from_opened_to_closed()

class ClosedDoorState(DoorState):
  def goto_opening(self,a_cabin_door):
   a_cabin_door.go_from_closed_to_opening()
  def goto_opened(self,a_cabin_door):
   a_cabin_door.go_from_closed_to_opened()
  def goto_closing(self,a_cabin_door):
   a_cabin_door.go_from_closed_to_closing()
  def goto_closed(self,a_cabin_door):
   a_cabin_door.go_from_closed_to_closed()

class OpeningDoorState(DoorState):
  def goto_opening(self,a_cabin_door):
   a_cabin_door.go_from_opening_to_opening()
  def goto_opened(self,a_cabin_door):
   a_cabin_door.go_from_opening_to_opened()
  def goto_closing(self,a_cabin_door):
   a_cabin_door.go_from_opening_to_closing()
  def goto_closed(self,a_cabin_door):
   a_cabin_door.go_from_opening_to_closed()

class ClosingDoorState(DoorState):
  def goto_opening(self,a_cabin_door):
   a_cabin_door.go_from_closing_to_opening()
  def goto_opened(self,a_cabin_door):
   a_cabin_door.go_from_closing_to_opened()
  def goto_closing(self,a_cabin_door):
   a_cabin_door.go_from_closing_to_closing()
  def goto_closed(self,a_cabin_door):
   a_cabin_door.go_from_closing_to_closed()
