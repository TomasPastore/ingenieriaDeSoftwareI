require './object'

class CabinDoorState

  def initialize(cabin_door)
    @cabin_door = cabin_door
  end

  def close_button_pressed
    should_be_implemented
  end

  def open_button_pressed
    should_be_implemented
  end

  def closed_sensor_activated
    should_be_implemented
  end

  def opened_sensor_activated
    should_be_implemented
  end

  def is_opened?
    false
  end

  def is_closed?
    false
  end

  def is_opening?
    false
  end

  def is_closing?
    false
  end

  def accept(visitor)
    should_be_implemented
  end

end