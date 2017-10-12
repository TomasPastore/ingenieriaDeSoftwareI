require './motor_stopped'
require './motor_moving_clockwise'
require './motor_moving_counter_clockwise'

class Motor
  NOT_STOPPED = 'Motor is not stopped'
  ALREADY_STOPPED = 'Motor is already stopped'
  ALREADY_MOVING_CLOCKWISE = 'Motor is already moving clockwise'
  ALREADY_MOVING_COUNTER_CLOCKWISE = 'Motor is already moving counter clockwise'

  def initialize
    @observers = []
    change_state_to_stopped
  end

  def add_state_observer(an_observer)
    @observers << an_observer
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

  private

  def change_state_to_stopped
    @observers.each do |an_observer|
      an_observer.visit_motor_stopped(@state)
    end

    change_state_to(MotorStopped.new(self))
  end

  def change_state_to_moving_clockwise
    @observers.each do |an_observer|
      an_observer.visit_motor_moving_clockwise(@state)
    end

    change_state_to(MotorMovingClockwise.new(self))
  end

  def change_state_to_moving_counter_clockwise
    @observers.each do |an_observer|    
      an_observer.visit_motor_moving_counter_clockwise(@state)
    end

    change_state_to(MotorMovingCounterClockwise.new(self))
  end

  def change_state_to(new_state)
    @state = new_state
  end

end