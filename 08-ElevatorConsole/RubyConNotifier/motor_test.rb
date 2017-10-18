require 'minitest/autorun'
require 'minitest/reporters'
require './motor'

MiniTest::Reporters.use!

class MotorTest < Minitest::Test
  def setup
    @motor = Motor.new
  end

  def test_01_motor_is_stopped_when_created
    assert(@motor.is_stopped?)
  end

  def test_02_motor_can_move_clockwise
    @motor.start_moving_clockwise

    assert(@motor.is_moving_clockwise?)
    assert(!@motor.is_stopped?)
  end

  def test_03_motor_can_move_counter_clockwise
    @motor.start_moving_counter_clockwise

    assert(@motor.is_moving_counter_clockwise?)
    assert(!@motor.is_moving_clockwise?)
    assert(!@motor.is_stopped?)
  end

  def test_04_motor_can_not_be_moving_clockwise_when_starting_to_move_clockwise
    @motor.start_moving_clockwise

    exception = assert_raises(Exception) { @motor.start_moving_clockwise }
    assert_equal(exception.message, Motor::ALREADY_MOVING_CLOCKWISE)
  end

  def test_05_motor_can_not_be_moving_counter_clockwise_when_starting_to_move_clockwise
    @motor.start_moving_counter_clockwise

    exception = assert_raises(Exception) { @motor.start_moving_clockwise }
    assert_equal(exception.message, Motor::NOT_STOPPED)
  end

  def test_06_motor_can_not_be_moving_counter_clockwise_when_starting_to_move_counter_clockwise
    @motor.start_moving_counter_clockwise

    exception = assert_raises(Exception) { @motor.start_moving_counter_clockwise }
    assert_equal(exception.message, Motor::ALREADY_MOVING_COUNTER_CLOCKWISE)
  end

  def test_07_motor_has_to_be_stopped_when_starting_to_move_counter_clockwise
    @motor.start_moving_clockwise

    exception = assert_raises(Exception) { @motor.start_moving_counter_clockwise }
    assert_equal(exception.message, Motor::NOT_STOPPED)
  end

  def test_08_can_stop_motor_when_moving
    @motor.start_moving_clockwise
    @motor.stop

    assert(@motor.is_stopped?)
  end

  def test_09_can_not_stop_motor_when_stopped
    exception = assert_raises(Exception) { @motor.stop }
    assert_equal(exception.message, Motor::ALREADY_STOPPED)
  end

end
