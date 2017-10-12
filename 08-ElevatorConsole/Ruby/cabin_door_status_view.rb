class CabinDoorStatusView

  def initialize(cabin_door)
    @cabin_door_state_model = ''
    @motor_state_model = ''
    cabin_door.add_state_observer(self)
  end

  def cabin_door_state_model
    @cabin_door_state_model
  end

  def motor_state_model
    @motor_state_model
  end

  def visit_motor_moving_clockwise(state)
    @motor_state_model = 'Moviendose en sentido de agujas de reloj'
  end

  def visit_motor_moving_counter_clockwise(state)
    @motor_state_model = 'Moviendose en sentido opuesto a las agujas de reloj'
  end

  def visit_motor_stopped(state)
    @motor_state_model = 'Parado'
  end

  def visit_cabin_door_closing(state)
    @cabin_door_state_model = 'Cerrandose'
  end

  def visit_cabin_door_closed(state)
    @cabin_door_state_model = 'Cerrada'
  end

  def visit_cabin_door_opening(state)
    @cabin_door_state_model = 'Abriendose'
  end

  def visit_cabin_door_opened(state)
    @cabin_door_state_model = 'Abierta'
  end
end