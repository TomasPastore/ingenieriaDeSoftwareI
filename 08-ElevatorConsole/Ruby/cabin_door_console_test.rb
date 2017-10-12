require 'minitest/autorun'
require 'minitest/reporters'
require './cabin_door'
require './cabin_door_console'
require './cabin_door_status_view'

MiniTest::Reporters.use!

class CabinDoorConsoleTest < Minitest::Test

  def test_01_console_logs_closing_event
    cabin_door = CabinDoor.new(Motor.new,self)
    console = CabinDoorConsole.new(cabin_door)
    cabin_door.close_button_pressed

    assert_closing_sequence_for(console)
  end

  def test_02_console_logs_closed_event
    cabin_door = CabinDoor.new(Motor.new,self)
    console = CabinDoorConsole.new(cabin_door)
    cabin_door.close_button_pressed
    cabin_door.closed_sensor_activated

    assert_closing_closed_sequence_for(console)
  end

  def test_03_console_logs_opening_event
    cabin_door = CabinDoor.new(Motor.new,self)
    console = CabinDoorConsole.new(cabin_door)
    cabin_door.close_button_pressed
    cabin_door.open_button_pressed

    assert_closing_opening_sequence_for(console)
  end

  def test_04_console_logs_opened_event
    cabin_door = CabinDoor.new(Motor.new,self)
    console = CabinDoorConsole.new(cabin_door)
    cabin_door.close_button_pressed
    cabin_door.open_button_pressed
    cabin_door.opened_sensor_activated

    assert_closing_opening_opened_sequence_for(console)
  end

  def test_05_status_view_shows_right_status_for_close_event_without_affecting_console
    cabin_door = CabinDoor.new(Motor.new,self)
    console = CabinDoorConsole.new(cabin_door)
    status_view = CabinDoorStatusView.new(cabin_door)
    cabin_door.close_button_pressed

    assert_closing_sequence_for(console)

    assert_equal('Moviendose en sentido de agujas de reloj',status_view.motor_state_model)
    assert_equal('Cerrandose',status_view.cabin_door_state_model)
  end

  def test_06_status_view_shows_right_status_for_open_event_without_affecting_console
    cabin_door = CabinDoor.new(Motor.new,self)
    console = CabinDoorConsole.new(cabin_door)
    status_view = CabinDoorStatusView.new(cabin_door)
    cabin_door.close_button_pressed
    cabin_door.open_button_pressed

    assert_closing_opening_sequence_for(console)

    assert_equal('Moviendose en sentido opuesto a las agujas de reloj',status_view.motor_state_model)
    assert_equal('Abriendose',status_view.cabin_door_state_model)

  end

  def test_07_status_view_shows_right_status_for_opened_event_without_affecting_console
    cabin_door = CabinDoor.new(Motor.new,self)
    console = CabinDoorConsole.new(cabin_door)
    status_view = CabinDoorStatusView.new(cabin_door)
    cabin_door.close_button_pressed
    cabin_door.open_button_pressed
    cabin_door.opened_sensor_activated

    assert_closing_opening_opened_sequence_for(console)

    assert_equal('Parado',status_view.motor_state_model)
    assert_equal('Abierta',status_view.cabin_door_state_model)
  end

  def test_08_status_view_shows_right_status_for_closed_event_without_affecting_console
    cabin_door = CabinDoor.new(Motor.new,self)
    console = CabinDoorConsole.new(cabin_door)
    status_view = CabinDoorStatusView.new(cabin_door)
    cabin_door.close_button_pressed
    cabin_door.closed_sensor_activated

    assert_closing_closed_sequence_for(console)

    assert_equal('Parado',status_view.motor_state_model)
    assert_equal('Cerrada',status_view.cabin_door_state_model)
  end

  def assert_closing_sequence_for(console)
    lines = console.lines_enumerator
    assert_equal(2, lines.size)
    assert_closing_sequence_on(lines)
  end

  def assert_closing_closed_sequence_for(console)
    lines = console.lines_enumerator
    assert_equal(4, lines.size)
    assert_closing_sequence_on(lines)
    assert_closed_sequence_on(lines)
  end

  def assert_closing_opening_sequence_for(console)
    lines = console.lines_enumerator
    assert_equal(5, lines.size)
    assert_closing_sequence_on(lines)
    assert_opening_when_closing_sequence_on(lines)
  end

  def assert_closing_opening_opened_sequence_for(console)
    lines = console.lines_enumerator
    assert_equal(7, lines.size)
    assert_closing_sequence_on(lines)
    assert_opening_when_closing_sequence_on(lines)
    assert_opened_sequence_on(lines)
  end

  def assert_closing_sequence_on(lines)
    assert_equal('Motor is moving clockwise',lines.next)
    assert_equal('Door is closing',lines.next)
  end

  def assert_closed_sequence_on(lines)
    assert_equal('Motor is stopped',lines.next)
    assert_equal('Door is closed',lines.next)
  end

  def assert_opening_when_closing_sequence_on(lines)
    assert_equal('Motor is stopped',lines.next)
    assert_equal('Motor is moving counter clockwise',lines.next)
    assert_equal('Door is opening',lines.next)
  end

  def assert_opened_sequence_on(lines)
    assert_equal('Motor is stopped',lines.next)
    assert_equal('Door is opened',lines.next)
  end

  def ring
  end

end
