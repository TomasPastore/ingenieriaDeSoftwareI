#For Python this file uses encoding: utf-8
    '''
    def openDoorIfSameFloor(self,aFloor):
        self._state.openDoorIfSameFloor(self,aFloor)
    
    def open_door_if_same_floor_when_moving_up(self,floor):
        pass
    def open_door_if_same_floor_when_moving_down(self,floor):
        pass
    def open_door_if_same_floor_when_stopped(self,floor):
        if floor == self.currentFloor()
            self.open_button_pressed()
       '''     

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
        return self.isMovingUp() or self.isMovingDown()
    def isMovingUp(self):
        return self._state.is_moving_up()
    def isMovingDown(self):
        return self._state.is_moving_down()
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

    def assertNotSkippingFloors(floor):
        self._state.assert_not_skipping_floors(self,floor)


    def assert_not_skipping_when_moving_up(self, floor):
        if floor != self.currentFloor+1:
            raise ElevatorEmergency(self.__class__.CABIN_SENSORS_NOT_SYNCHRONIZED)

    def assert_not_skipping_when_moving_down(self, floor):
        if floor+1 != self.currentFloor:
            raise ElevatorEmergency(self.__class__.CABIN_SENSORS_NOT_SYNCHRONIZED)

    def assert_not_skipping_when_stopped(self, floor):
        if self.currentFloor() != floor:
            raise ElevatorEmergency(self.__class__.CABIN_SENSORS_NOT_SYNCHRONIZED)
    

    def open_command_when_stopped():
        self._door.open_button_pressed()

    def open_command_when_moving_up():
        pass
    def open_command_when_moving_down():
        pass
    


    def updateCurrentFloor(floor):
        self.assertNotSkippingFloors(floor) 
        self.currentFloor = floor

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
    def is_moving_up(self):
        self.should_be_implemented_by_subclass()
    def is_moving_down(self):
        self.should_be_implemented_by_subclass()
    def goto_moving_up(self,cabin):
        self.should_be_implemented_by_subclass()
    def goto_moving_down(self,cabin):
        self.should_be_implemented_by_subclass()    
    def goto_stopped(self,cabin):
        self.should_be_implemented_by_subclass()
    def assert_not_skipping_floors(self,floor)
        self.should_be_implemented_by_subclass()
    
    def should_be_implemented_by_subclass():
        raise NotImplementedError("Subclass responsibility")

class MovingUpCabinState(CabinState):
    def is_moving_up(self):
        return True
    def is_moving_down(self):
        return False
    def is_stopped(self):
        return False
    def goto_moving_up(self,cabin):
        cabin.goto_moving_up_from_moving_up()
    def goto_moving_down(self,cabin):
        cabin.goto_moving_down_from_moving_up()
    def goto_stopped(self,cabin):
        cabin.goto_stopped_from_moving_up()
    def open_command_issued(self,cabin):
        cabin.open_command_when_moving_up()
    def assert_not_skipping_floors(self,a_cabin,floor):
        a_cabin.assert_not_skipping_floors_when_moving_up(floor)

class MovingDownCabinState(CabinState):
    def is_moving_up(self):
        return False
    def is_moving_down(self):
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
    def assert_not_skipping_floors(self,a_cabin,floor):
        a_cabin.assert_not_skipping_floors_when_moving_down(floor)
    
class StoppedCabinState(CabinState):
    def is_moving_up(self):
        return False
    def is_moving_down(self):
        return False
    def is_stopped(self):
        return True
    def goto_moving(self,cabin):
        cabin.goto_moving_from_stopped()
    def goto_stopped(self,cabin):
        cabin.goto_stopped_from_stopped()
    def open_command_issued(self,cabin):
        cabin.open_command_when_stoppped()
    def assert_not_skipping_floors(self,a_cabin,floor):
        a_cabin.assert_not_skipping_floors_when_stopped(floor)


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