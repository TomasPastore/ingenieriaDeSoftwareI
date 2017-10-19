require './motor_stopped'
require './motor_moving_clockwise'
require './motor_moving_counter_clockwise'
require './notifier'

class Motor
  NOT_STOPPED = 'Motor is not stopped'
  ALREADY_STOPPED = 'Motor is already stopped'
  ALREADY_MOVING_CLOCKWISE = 'Motor is already moving clockwise'
  ALREADY_MOVING_COUNTER_CLOCKWISE = 'Motor is already moving counter clockwise'

  def initialize
    @observers_notifier = Notifier.new
    change_state_to_stopped
  end

  def is_stopped?
    @state.is_stopped?
  end

  def is_moving_clockwise?
    @state.is_moving_clockwise?
  end

  def is_moving_counter_clockwise?
    @state.is_moving_counter_clockwise?
  end

  def stop
    @state.stop
  end

  def stop_when_stopped
    raise Exception.new(ALREADY_STOPPED)
  end

  def stop_when_moving_clockwise
    change_state_to_stopped
  end

  def stop_when_moving_counter_clockwise
    change_state_to_stopped
  end

  def start_moving_clockwise
    @state.start_moving_clockwise
  end

  def start_moving_clockwise_when_stopped
    change_state_to_moving_clockwise
  end

  def start_moving_clockwise_when_moving_clockwise
    raise Exception.new(ALREADY_MOVING_CLOCKWISE)
  end

  def start_moving_clockwise_when_moving_counter_clockwise
    raise Exception.new(NOT_STOPPED)
  end

  def start_moving_counter_clockwise
    @state.start_moving_counter_clockwise
  end

  def start_moving_counter_clockwise_when_stopped
    change_state_to_moving_counter_clockwise
  end

  def start_moving_counter_clockwise_when_moving_clockwise
    raise Exception.new(NOT_STOPPED)
  end

  def start_moving_counter_clockwise_when_moving_counter_clockwise
    raise Exception.new(ALREADY_MOVING_COUNTER_CLOCKWISE)
  end

  def admit_as_observer(observer)
    @observers_notifier.register(observer)
  end

  def remove_observer(observer)
    @observers_notifier.unregister(observer)
  end

  private

  def change_state_to_stopped
    change_state_and_ask_to_notify(MotorStopped.new(self))
  end

  def change_state_to_moving_clockwise
    change_state_and_ask_to_notify(MotorMovingClockwise.new(self))
  end

  def change_state_to_moving_counter_clockwise
    change_state_and_ask_to_notify(MotorMovingCounterClockwise.new(self))
  end

  def change_state_to(new_state)
    @state = new_state
  end

  def change_state_and_ask_to_notify(new_state)
    @state = new_state
    @state.ask_notifier_to_notify_observers(@observers_notifier)
  end

end