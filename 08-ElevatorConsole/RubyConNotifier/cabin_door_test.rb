require 'minitest/autorun'
require 'minitest/reporters'
require './cabin_door'

MiniTest::Reporters.use!

class CabinDoorTest < Minitest::Test

  def setup
    @door = CabinDoor.new(Motor.new,self)
    @ringed = false
  end

  def ring
    @ringed = true
  end

  def test_01_door_is_open_when_created
    assert_door_is_opened
  end

  def test_02_door_start_closing_when_close_pressed
    @door.close_button_pressed
    assert_door_is_closing
  end

  def test_03_when_closing_is_ok_to_press_close
    @door.close_button_pressed
    assert_should_not_raise(Exception) { @door.close_button_pressed }
    assert_has_ringed_the_bell
  end

  def test_04_door_stops_closing_when_closing_and_closed_sensor_is_activated
    @door.close_button_pressed
    @door.closed_sensor_activated
    assert_door_is_closed
  end

  def test_05_door_starts_opening_when_closing_and_open_is_pressed
    @door.close_button_pressed
    @door.open_button_pressed
    assert_door_is_opening
  end

  def test_06_when_opening_is_ok_to_press_open
    @door.close_button_pressed
    @door.open_button_pressed

    assert_should_not_raise(Exception) { @door.open_button_pressed }
    assert_has_ringed_the_bell
  end

  def test_07_can_close_when_opening
    @door.close_button_pressed
    @door.open_button_pressed
    @door.close_button_pressed

    assert_door_is_closing
  end

  def test_08_close_does_nothing_when_closed
    @door.close_button_pressed
    @door.closed_sensor_activated
    assert_should_not_raise(Exception) { @door.close_button_pressed }
    assert_has_ringed_the_bell
  end

  def test_09_open_does_nothing_when_opened
    assert_should_not_raise(Exception) { @door.open_button_pressed }
    assert_has_ringed_the_bell
  end

  def test_10_open_does_nothing_when_closed
    @door.close_button_pressed
    @door.closed_sensor_activated
    assert_should_not_raise(Exception) { @door.open_button_pressed }
    assert_has_ringed_the_bell
  end

  def test_11_closed_sensor_malfunction_if_activated_when_opened
    assert_raises_with_message(Exception,CabinDoor::CLOSED_SENSOR_MALFUNCTION) { @door.closed_sensor_activated }
  end

  def test_12_closed_sensor_malfunction_if_activated_when_opening
    @door.close_button_pressed
    @door.open_button_pressed

    assert_raises_with_message(Exception,CabinDoor::CLOSED_SENSOR_MALFUNCTION) { @door.closed_sensor_activated }
  end

  def test_13_closed_sensor_malfunction_if_activated_when_closed
    @door.close_button_pressed
    @door.closed_sensor_activated

    assert_raises_with_message(Exception,CabinDoor::CLOSED_SENSOR_MALFUNCTION) { @door.closed_sensor_activated }
  end

  def test_14_stops_opening_when_opened_sensor_is_activated
    @door.close_button_pressed
    @door.open_button_pressed
    @door.opened_sensor_activated

    assert_door_is_opened
  end

  def test_15_opened_sensor_malfunction_if_activated_when_opened
    assert_raises_with_message(Exception,CabinDoor::OPENED_SENSOR_MALFUNCTION) { @door.opened_sensor_activated }
  end

  def test_16_opened_sensor_malfunction_if_activated_when_closed
    @door.close_button_pressed
    @door.closed_sensor_activated

    assert_raises_with_message(Exception,CabinDoor::OPENED_SENSOR_MALFUNCTION) { @door.opened_sensor_activated }
  end

  def test_17_opened_sensor_malfunction_if_activated_when_closing
    @door.close_button_pressed

    assert_raises_with_message(Exception,CabinDoor::OPENED_SENSOR_MALFUNCTION) { @door.opened_sensor_activated }
  end

  def assert_raises_with_message(exception_type,message,&block)
    exception = assert_raises(exception_type,&block)
    assert_equal(exception.message,message)
  end

  def assert_should_not_raise(exception_type,&block)
    begin
      block.call
    rescue exception_type
      fail 'Se levanto excepcion que no debia'
    end
  end

  def assert_has_ringed_the_bell
    assert(@ringed)
  end

  def assert_door_is_opened
    assert(@door.is_opened?)
    assert(@door.is_motor_stopped?)

    assert(!@door.is_closing?)
    assert(!@door.is_opening?)
    assert(!@door.is_closed?)
  end

  def assert_door_is_closing
    assert(@door.is_closing?)
    assert(@door.is_motor_moving_clockwise?)

    assert(!@door.is_opened?)
    assert(!@door.is_opening?)
    assert(!@door.is_closed?)
  end

  def assert_door_is_closed
    assert(@door.is_closed?)
    assert(@door.is_motor_stopped?)

    assert(!@door.is_opened?)
    assert(!@door.is_opening?)
    assert(!@door.is_closing?)
  end

  def assert_door_is_opening
    assert(@door.is_opening?)
    assert(@door.is_motor_moving_counter_clockwise?)

    assert(!@door.is_opened?)
    assert(!@door.is_closing?)
    assert(!@door.is_closed?)
  end
end