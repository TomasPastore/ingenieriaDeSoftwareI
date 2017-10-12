require './cabin_door_state'

class CabinDoorOpened < CabinDoorState

  def is_opened?
    true
  end

  def close_button_pressed
    @cabin_door.close_button_pressed_when_opened
  end

  def open_button_pressed
    @cabin_door.open_button_pressed_when_opened
  end

  def closed_sensor_activated
    @cabin_door.closed_sensor_activated_when_opened
  end

  def opened_sensor_activated
    @cabin_door.opened_sensor_activated_when_opened
  end

  def accept(visitor)
    visitor.visit_cabin_door_opened(self)
  end

end
