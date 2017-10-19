class CabinDoorStatusView

  def initialize(cabin_door)
    @cabin_door_state_model = ''
    @motor_state_model = ''
    cabin_door.admit_as_observer(self)
  end

  def cabin_door_state_model
    @cabin_door_state_model
  end

  def motor_state_model
    @motor_state_model
  end

  def get_notification(notification_origin)
    notification_origin.update(self)
  end

  def update_when_motor_moving_clockwise
    @motor_state_model = 'Moviendose en sentido de agujas de reloj'
  end

  def update_when_motor_moving_counter_clockwise
    @motor_state_model = 'Moviendose en sentido opuesto a las agujas de reloj'
  end

  def update_when_motor_stopped
    @motor_state_model = 'Parado'
  end

  def update_when_cabin_door_closing
    @cabin_door_state_model = 'Cerrandose'
  end

  def update_when_cabin_door_closed
    @cabin_door_state_model = 'Cerrada'
  end

  def update_when_cabin_door_opening
    @cabin_door_state_model = 'Abriendose'
  end

  def update_when_cabin_door_opened
    @cabin_door_state_model = 'Abierta'
  end
end