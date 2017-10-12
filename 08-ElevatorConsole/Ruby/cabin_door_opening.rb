require './cabin_door_state'

class CabinDoorOpening < CabinDoorState

  def is_opening?
    true
  end

  def open_button_pressed
    @cabin_door.open_button_pressed_when_opening
  end

  def close_button_pressed
    @cabin_door.close_button_pressed_when_opening
  end

  def closed_sensor_activated
    @cabin_door.closed_sensor_activated_when_opening
  end

  def opened_sensor_activated
    @cabin_door.opened_sensor_activated_when_opening
  end

  def accept(visitor)
    visitor.visit_cabin_door_opening(self)
  end
end

