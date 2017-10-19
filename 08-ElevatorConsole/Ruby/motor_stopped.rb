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

  def ask_notifier_to_notify_observers(a_notifier)
    a_notifier.notify_observers(self)
  end

  def update(an_allowed_observer)
    an_allowed_observer.update_when_motor_stopped
  end
  
end
