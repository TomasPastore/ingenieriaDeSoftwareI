require './motor_state'

class MotorMovingClockwise < MotorState

  def is_moving_clockwise?
    true
  end

  def stop
    @motor.stop_when_moving_clockwise
  end

  def start_moving_clockwise
    @motor.start_moving_clockwise_when_moving_clockwise
  end

  def start_moving_counter_clockwise
    @motor.start_moving_counter_clockwise_when_moving_clockwise
  end

  def accept(visitor)
    visitor.visit_motor_moving_clockwise(self)
  end
end
