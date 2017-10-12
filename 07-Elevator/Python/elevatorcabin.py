#For Python this file uses encoding: utf-8

import unittest
from elevatorcabindoor import ElevatorCabinDoor
from elevatoremergency import ElevatorEmergency

#^ eso es provicional... En sí se me ocurre la opción de que el ElevatorController les pase la clase... Pero no sé

class ElevatorCabin(object):
    def __init__(self):
        self.MOVING_UP = MovingUpCabinState()
        self.MOVING_DOWN = MovingDownCabinState()
        self.STOPPED = StoppedCabinState()
        self._state = self.STOPPED
        self._door = ElevatorCabinDoor()
        self._currentFloor = 0

    def waitForPeopleTimedOut():
        self._door.wait_for_people_timed_out()
    def isStopped(self):
        return self._state.is_stopped()
    def isMoving(self):
        return self._state.is_moving()
    def isDoorOpened(self):
        return self._door.is_opened()
    def isDoorOpening(self):
        return self._door.is_opening()
    def isDoorClosed(self):
        return self._door.is_closed()
    def isDoorClosing(self):
        return self._door.is_closing()
    def doorIsClosed(self):
        self._door.closed_sensor_signal()
    def doorIsOpened(self):
        self._door.opened_sensor_signal()
    def currentFloor(self):
    	self._currentFloor
    def moveUp(self):
        self._state.goto_moving_up(self)
    def stop(self):
        self._state.goto_stopped(self)
    def closeCommandIssued(self):
        self._door.close_button_pressed()
    def openCommandIssued(self):
        self._state.open_command_issued()

    def isSkippingFloors(floor):
        self._state.is_skipping_floors(self,floor)

    def is_skipping_when_moving_up(floor):
        return floor-1 != self.currentFloor

    def is_skipping_when_moving_down(floor):
        return floor+1 != self.currentFloor

    def is_skipping_when_stopped(floor):
        return False

    def open_command_when_stopped():
        self._door.open_button_pressed()

    def open_command_when_moving():
        raise ElevatorEmergency(self.__class__.CABIN_SENSORS_NOT_SYNCHRONIZED)
    

    def updateCurrentFloor(floor):
        
        if self.currentFloor() != floor:
            raise ElevatorEmergency(self.__class__.CABIN_SENSORS_NOT_SYNCHRONIZED)
        self.currentFloor = floor

        if floor == self.nextFloor() :

        #No estoy seguro de que esto realmente vaya acá :s
        #No es un estado de la cabina, creo :s
        #Se puede responder isSkippingFloors desde acá, seguro...
        #Pero no sé si tiene sentido que SKIPPINGFLOORS y GOINGINWRONGDIRECTION sean estados :s
        #Casi que me parece que tiene más sentido que sean estados del controller... Aunque tampoco
        if self.isCabinSkippingFloors(floor) or self.isCabingGoingInWrongDirection(floor):
            raise ElevatorEmergency(self.__class__.CABIN_SENSORS_NOT_SYNCHRONIZED)
        else:



    def goto_moving_up_from_stopped(self):
        self._state = self.MOVING_UP
    def goto_moving_up_from_moving_up(self):
        pass
    def goto_moving_up_from_moving_down(self):
        raise ElevatorEmergency(ElevatorEmergency.CABIN_SENSORS_NOT_SYNCHRONIZED)
    
    def goto_moving_down_from_stopped(self):
        self._state = self.MOVING_DOWN
    def goto_moving_down_from_moving_down(self):
        pass
    def goto_moving_down_from_moving_up(self):
        raise ElevatorEmergency(ElevatorEmergency.CABIN_SENSORS_NOT_SYNCHRONIZED)

    def goto_stopped_from_moving_up(self):
        self._state = self.STOPPED
    def goto_stopped_from_moving_down(self):
        self._state = self.STOPPED
    def goto_stopped_from_stopped(self):
        pass


class CabinState:
    def is_stopped(self):
        self.should_be_implemented_by_subclass()
    def is_moving(self):
        self.should_be_implemented_by_subclass()
    def goto_moving(self,cabin):
        self.should_be_implemented_by_subclass()
    def goto_stopped(self,cabin):
        self.should_be_implemented_by_subclass()
    def should_be_implemented_by_subclass():
        raise NotImplementedError("Subclass responsibility")

class MovingUpCabinState(CabinState):
    def is_moving(self):
        return True
    def is_stopped(self):
        return False
    def goto_moving_up(self,cabin):
        cabin.goto_moving_up_from_moving_up()
    def goto_moving_down(self,cabin):
        cabin.goto_moving_down_from_moving_up()
    def goto_stopped(self,cabin):
        cabin.goto_stopped_from_moving()
    def open_command_issued(self,cabin):
        cabin.open_command_when_moving()
    def is_skipping_floors(self,a_cabin,floor):
        a_cabin.is_skipping_when_moving_down(floor)


class MovingDownCabinState(CabinState):
    def is_moving(self):
        return True
    def is_stopped(self):
        return False
    def goto_moving_up(self,cabin):
        cabin.goto_moving_up_from_moving_down()
    def goto_moving_down(self,cabin):
        cabin.goto_moving_down_from_moving_down()
    def goto_stopped(self,cabin):
        cabin.goto_stopped_from_moving()
    def open_command_issued(self,cabin):
        cabin.open_command_when_moving()
    def is_skipping_floors(self,a_cabin,floor):
        a_cabin.is_skipping_when_moving_down(floor)

class StoppedCabinState(CabinState):
    def is_moving(self):
        return False
    def is_stopped(self):
        return True
    def goto_moving(self,cabin):
        cabin.goto_moving_from_stopped()
    def goto_stopped(self,cabin):
        cabin.goto_stopped_from_stopped()
    def open_command_issued(self,cabin):
        cabin.open_command_when_stoppped()
    def is_skipping_floors(self,a_cabin,floor):
        a_cabin.is_skipping_when_stopped(floor)


class CabinTests(unittest.TestCase):
    def test01CabinStartsStopped(self):
        cabin = Cabin()
        self.assertTrue(cabin.isStopped())
        self.assertFalse(cabin.isMoving())
    def test02CabinDoorGetsToClosingWithCloseCommand(self):
        cabin = Cabin()
        cabin.closeCommandIssued()
        self.assertTrue(cabin.isDoorClosing())
        self.assertFalse(cabin.isDoorOpening())

if __name__ == '__main__':
    unittest.main()