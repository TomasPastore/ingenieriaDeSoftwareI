require './motor'
require './cabin_door_closed'
require './cabin_door_closing'
require './cabin_door_opened'
require './cabin_door_opening'

class CabinDoor

  CLOSED_SENSOR_MALFUNCTION = 'Funcionamiento incorrecto del sensor de puerta cerrada'
  OPENED_SENSOR_MALFUNCTION = 'Funcionamiento incorrecto del sensor de puerta abierta'

  def initialize(motor,bell)
    @motor = motor
    @bell = bell
    #uso uno distinto al del motor porque eventualmente puede sumarse un observador 
    #que no quiera ser notificado por ambos modulos
    @observers_notifier = Notifier.new
    change_state_to_opened
  end

  #Testing state
  def is_opened?
    @state.is_opened?
  end

  def is_closing?
    @state.is_closing?
  end

  def is_opening?
    @state.is_opening?
  end

  def is_closed?
    @state.is_closed?
  end

  #Campana
  def ring
    @bell.ring
  end

  #Boton de cerrar
  def close_button_pressed
    @state.close_button_pressed
  end

  def close_button_pressed_when_opened
    start_closing_door
  end

  def close_button_pressed_when_closing
    #ya estoy cerrando la puerta, no tengo que hacer nada con el motor
    ring
  end

  def close_button_pressed_when_opening
    @motor.stop
    start_closing_door
  end

  def close_button_pressed_when_closed
    #la puerta ya esta cerrada, no hay que hacer nada
    ring
  end

  #Boton de abrir
  def open_button_pressed
    @state.open_button_pressed
  end

  def open_button_pressed_when_closing
    @motor.stop
    start_opening_door
  end

  def open_button_pressed_when_opening
    #ya estoy abriendo la puerta, no tengo que hacer nada
    ring
  end

  def open_button_pressed_when_opened
    #la puerta ya esta abierta, no hago nada
    ring
  end

  def open_button_pressed_when_closed
    #la puerta esta cerrada, no se puede abrir
    ring
  end

  #Sensor de puerta cerrada
  def closed_sensor_activated
    @state.closed_sensor_activated
  end

  def closed_sensor_activated_when_closing
    @motor.stop
    change_state_to_closed
  end

  def closed_sensor_activated_when_opened
    raise_closed_sensor_malfunction
  end

  def closed_sensor_activated_when_opening
    raise_closed_sensor_malfunction
  end

  def closed_sensor_activated_when_closed
    raise_closed_sensor_malfunction
  end

  #Sensor de puerta abierta
  def opened_sensor_activated
    @state.opened_sensor_activated
  end

  def opened_sensor_activated_when_opening
    @motor.stop
    change_state_to_opened
  end

  def opened_sensor_activated_when_opened
    raise_opened_sensor_malfunction
  end

  def opened_sensor_activated_when_closed
    raise_opened_sensor_malfunction
  end

  def opened_sensor_activated_when_closing
    raise_opened_sensor_malfunction
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

  def admit_as_observer(observer)
    @observers_notifier.register(observer)
    @motor.admit_as_observer(observer)
  end

  def remove_observer(observer)
    @observers_notifier.unregister(observer)
    @motor.remove_observer(observer)
  end

  private

  def start_closing_door
    @motor.start_moving_clockwise
    change_state_to_closing
  end

  def start_opening_door
    @motor.start_moving_counter_clockwise
    change_state_to_opening
  end

  def change_state_to_closing
    change_state_and_ask_to_notify(CabinDoorClosing.new(self))
  end

  def change_state_to_opening
    change_state_and_ask_to_notify(CabinDoorOpening.new(self))
  end

  def change_state_to_closed
    change_state_and_ask_to_notify(CabinDoorClosed.new(self))
  end

  def change_state_to_opened
    change_state_and_ask_to_notify(CabinDoorOpened.new(self))
  end

  def change_state_to(new_state)
    @state = new_state
  end

  def change_state_and_ask_to_notify(new_state)
    @state = new_state
    @state.ask_notifier_to_notify_observers(@observers_notifier)
  end

  def raise_closed_sensor_malfunction
    raise Exception.new(CLOSED_SENSOR_MALFUNCTION)
  end

  def raise_opened_sensor_malfunction
    raise Exception.new(OPENED_SENSOR_MALFUNCTION)
  end

end