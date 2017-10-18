require './cabin_door_state'

class CabinDoorClosing < CabinDoorState

  def is_closing?
    true
  end

  def close_button_pressed
    @cabin_door.close_button_pressed_when_closing
  end

  def open_button_pressed
    @cabin_door.open_button_pressed_when_closing
  end

  def closed_sensor_activated
    @cabin_door.closed_sensor_activated_when_closing
  end

  def opened_sensor_activated
    @cabin_door.opened_sensor_activated_when_closing
  end

  def ask_notifier_to_notify_observers(a_notifier)
    a_notifier.notify_observers(self)
  end

  def update(an_allowed_observer)
    an_allowed_observer.update_when_cabin_door_closing
  end
end

