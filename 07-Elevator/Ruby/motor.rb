class Motor
  STOPPED = 1
  MOVING_CLOCKWISE = 2
  MOVING_COUNTER_CLOCKWISE = 3

  NOT_STOPPED = 'Motor is not stopped'
  ALREADY_STOPPED = 'Motor is already stopped'
  ALREADY_MOVING_CLOCKWISE = 'Motor is already moving clockwise'
  ALREADY_MOVING_COUNTER_CLOCKWISE = 'Motor is already moving counter clockwise'

  def initialize
    @state = STOPPED
  end

  def is_stopped?
    @state == STOPPED
  end

  def is_moving_clockwise?
    @state == MOVING_CLOCKWISE
  end

  def is_moving_counter_clockwise?
    @state == MOVING_COUNTER_CLOCKWISE
  end

  def stop
    assert_is_not_stopped
    #aca habria que mandar el output correspondiente para parar el motor
    @state = STOPPED
  end

  def start_moving_clockwise
    assert_is_not_moving_clockwise
    assert_is_stopped
    #aca habria que mandar el output correspondiente para mover el motor en
    #sentido de las agujas del relog
    @state = MOVING_CLOCKWISE
  end

  def start_moving_counter_clockwise
    assert_is_not_moving_counter_clockwise
    assert_is_stopped
    #aca habria que mandar el output correspondiente para mover el motor en
    #sentido contrario de las agujas del relog
    @state = MOVING_COUNTER_CLOCKWISE
  end

  def assert_is_not_stopped
    raise Exception.new(ALREADY_STOPPED) if is_stopped?
  end

  def assert_is_not_moving_clockwise
    raise Exception.new(ALREADY_MOVING_CLOCKWISE) if is_moving_clockwise?
  end

  def assert_is_not_moving_counter_clockwise
    raise Exception.new(ALREADY_MOVING_COUNTER_CLOCKWISE) if is_moving_counter_clockwise?
  end

  def assert_is_stopped
    raise Exception.new(NOT_STOPPED) if !is_stopped?
  end
end