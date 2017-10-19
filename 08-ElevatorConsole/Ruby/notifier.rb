class Notifier

    def initialize()
        @observers = []
    end

    def observers
        @observers
    end

    def notify_observers(notification_origin)
        for an_observer in @observers
            notify_observer(an_observer,notification_origin)
        end
    end

    def notify_observer(an_observer,notification_origin)
        an_observer.get_notification(notification_origin)
    end

    def register(an_observer)
        @observers << an_observer
    end

    def unregister(an_observer)
        @observers.delete(an_observer)
    end
end