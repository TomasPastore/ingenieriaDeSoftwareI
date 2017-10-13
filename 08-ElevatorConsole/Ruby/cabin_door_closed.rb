require './cabin_door_state'

class CabinDoorClosed < CabinDoorState

  def is_closed?
    true
  end

  def close_button_pressed
    @cabin_door.close_button_pressed_when_closed
  end

  def open_button_pressed
    @cabin_door.open_button_pressed_when_closed
  end

  def closed_sensor_activated
    @cabin_door.closed_sensor_activated_when_closed
  end

  def opened_sensor_activated
    @cabin_door.opened_sensor_activated_when_closed
  end

  def accept(visitor)
    visitor.visit_cabin_door_closed(self)
  end
end