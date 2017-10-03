require './motor'

class CabinDoor

  CLOSED_SENSOR_MALFUNCTION = 'Funcionamiento incorrecto del sensor de puerta cerrada'
  OPENED_SENSOR_MALFUNCTION = 'Funcionamiento incorrecto del sensor de puerta abierta'

  def initialize(motor,bell)
    @motor = motor
    @bell = bell
    @state = :open
    @counter = 0
  end

  def should_implement
    raise 'Implementar!'
  end

  #Testing state
  def is_opened?
    @state == :open
  end

  def is_closing?
    @state == :closing
  end

  def is_opening?
    @state == :opening
  end

  def is_closed?
    @state == :closed
  end

  #Campana
  def ring
    @bell.ring
  end

  #Boton de cerrar
  def close_button_pressed
    unless self.is_closing?
      @motor.stop if self.is_opening?
      @state = :closing
      @motor.start_moving_clockwise
    end
    @bell.ring
  end

  #Boton de abrir
  def open_button_pressed
    @state = @state.goto_opening
    unless self.is_opening?
      @motor.stop if self.is_closing?
      @state = :opening
      @motor.start_moving_counter_clockwise
    end
    @bell.ring
  end

  #Sensor de puerta cerrada
  def closed_sensor_activated
    raise CLOSED_SENSOR_MALFUNCTION unless self.is_closing?
    @state = :closed
    @motor.stop
  end

  #Sensor de puerta abierta
  def opened_sensor_activated
    raise OPENED_SENSOR_MALFUNCTION unless self.is_opening?
    @state = :open
    @motor.stop
  end

  #Motor
  def is_motor_stopped?
    @motor.is_stopped?
  end

  def is_motor_moving_clockwise?
    @motor.is_moving_clockwise?
  end

  def is_motor_moving_counter_clockwise?
    @motor.is_moving_counter_clockwise?
  end

end
