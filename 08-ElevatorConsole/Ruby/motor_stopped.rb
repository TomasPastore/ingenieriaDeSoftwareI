require './motor_state'

class MotorStopped < MotorState

  def is_stopped?
    true
  end

  def stop
    @motor.stop_when_stopped
  end

  def start_moving_clockwise
    @motor.start_moving_clockwise_when_stopped
  end

  def start_moving_counter_clockwise
    @motor.start_moving_counter_clockwise_when_stopped
  end

  def accept(visitor)
    visitor.visit_motor_stopped(self)
  end
end
