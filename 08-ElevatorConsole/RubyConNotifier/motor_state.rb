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

  def ask_notifier_to_notify_observers(a_notifier)
    should_be_implemented
  end

  def update(an_allowed_observer)
    should_be_implemented
  end

end