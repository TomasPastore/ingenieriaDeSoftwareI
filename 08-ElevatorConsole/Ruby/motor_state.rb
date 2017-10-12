require './object'

class MotorState

  def initialize(motor)
    @motor = motor
  end

  def is_stopped?
    false
  end

  def is_moving_clockwise?
    false
  end

  def is_moving_counter_clockwise?
    false
  end

  def stop
    should_be_implemented
  end

  def start_moving_clockwise
    should_be_implemented
  end

  def start_moving_counter_clockwise
    should_be_implemented
  end

  def accept(visitor)
    should_be_implemented
  end

end