class CabinDoorConsole

  def initialize(cabin_door)
    @lines = []
    cabin_door.admit_as_observer(self)
  end

  def lines_enumerator
    #@lines.each
    enumerator = @lines.enum_for(:each)
    #Esto es solamente para poder correrlo en el labo que usa ruby 1.9... En Ruby 2+ no hace falta...
    class << enumerator
      def size
        self.count
      end
    end
    enumerator
  end

  def get_notification(notification_origin)
    notification_origin.update(self)
  end

  def update_when_motor_moving_clockwise
    @lines << 'Motor is moving clockwise'
  end

  def update_when_motor_moving_counter_clockwise
    @lines << 'Motor is moving counter clockwise'
  end

  def update_when_motor_stopped
    @lines << 'Motor is stopped'
  end

  def update_when_cabin_door_closing
    @lines << 'Door is closing'
  end

  def update_when_cabin_door_closed
    @lines << 'Door is closed'
  end

  def update_when_cabin_door_opening
    @lines << 'Door is opening'
  end

  def update_when_cabin_door_opened
    @lines << 'Door is opened'
  end
end