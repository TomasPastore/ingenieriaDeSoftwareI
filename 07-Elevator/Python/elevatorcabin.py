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

    #Observadores
    def floorNumber(self):
        return self._currentFloor
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
    def isWaitingForPeople(self):
        return self._door.is_waiting_for_people()
    

    def doorIsClosed(self):
        self._door.closed_sensor_signal()
    def doorIsOpened(self):
        self._door.opened_sensor_signal()    
    def closeDoor(self):
        self._door.close_button_pressed()
    def waitForPeopleTimedOut(self):
        self._door.wait_for_people_timed_out()

    def openDoor(self):
        self._state.open_command_issued(self)
    def open_command_when_stopped(self):
        self._door.open_button_pressed()
    def open_command_when_moving_up(self):
        pass
    def open_command_when_moving_down(self):
        pass

    #Acciones
    def onFloor(self,aFloor):
        self.assertNotSkippingFloors(aFloor) 
        self._currentFloor = aFloor
    
    def gotoFloor(self,aFloor):
        self.closeDoor()
        if aFloor > self.floorNumber():
            self.moveUp()
        else:
            self.moveDown()

    def moveUp(self):
        self._state.goto_moving_up(self)
    def moveDown(self):
        self._state.goto_moving_down(self)
    def stop(self):
        self._state.goto_stopped(self)

    def goto_moving_up_from_stopped(self):
        self._state = self.MOVING_UP
    def goto_moving_up_from_moving_up(self):
        pass
    def goto_moving_up_from_moving_down(self):
        raise ElevatorEmergency(ElevatorEmergency.CABIN_SENSORS_NOT_SYNCHRONIZED)
        #podria ser stopped y despues move down

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
    
    #Otras 

    def protocolToAdd(self,anElevatorController,aFloor):
        if aFloor > self.floorNumber(): 
           return anElevatorController.protocolToAddWhenFloorIsUpwards()
        else:
           return anElevatorController.protocolToAddWhenFloorIsDownwards()
    
    def assertNotSkippingFloors(self,aSignaledFloor):
        self._state.assert_not_skipping_floors(self,aSignaledFloor)

    def assert_not_skipping_when_moving_up(self, aSignaledFloor):
        if aSignaledFloor-1 != self.floorNumber():
            raise ElevatorEmergency(ElevatorEmergency.CABIN_SENSORS_NOT_SYNCHRONIZED)
    def assert_not_skipping_when_moving_down(self, floor):
        if floor+1 != self.floorNumber():
            raise ElevatorEmergency(ElevatorEmergency.CABIN_SENSORS_NOT_SYNCHRONIZED)
    def assert_not_skipping_when_stopped(self, floor):
        if self.floorNumber() != floor:
            raise ElevatorEmergency(ElevatorEmergency.CABIN_SENSORS_NOT_SYNCHRONIZED)


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
    def open_command_issued(self,aCabin):
        self.should_be_implemented_by_subclass()
    def assert_not_skipping_floors(self,aCabin, aSignaledFloor):
        self.should_be_implemented_by_subclass()
   
    def should_be_implemented_by_subclass(self):
        raise NotImplementedError("Subclass responsibility")

class MovingUpCabinState(CabinState):
    def is_moving_up(self):
        return True
    def is_moving_down(self):
        return False
    def is_stopped(self):
        return False
    def goto_moving_up(self,aCabin):
        aCabin.goto_moving_up_from_moving_up()
    def goto_moving_down(self,aCabin):
        aCabin.goto_moving_down_from_moving_up()
    def goto_stopped(self,aCabin):
        aCabin.goto_stopped_from_moving_up()
    def open_command_issued(self,aCabin):
        aCabin.open_command_when_moving_up()
    def assert_not_skipping_floors(self,aCabin,aSignaledFloor):
        aCabin.assert_not_skipping_when_moving_up(aSignaledFloor)
    

class MovingDownCabinState(CabinState):
    def is_moving_up(self):
        return False
    def is_moving_down(self):
        return True
    def is_stopped(self):
        return False
    def goto_moving_up(self,aCabin):
        aCabin.goto_moving_up_from_moving_down()
    def goto_moving_down(self,aCabin):
        aCabin.goto_moving_down_from_moving_down()
    def goto_stopped(self,aCabin):
        aCabin.goto_stopped_from_moving_down()
    def open_command_issued(self,aCabin):
        aCabin.open_command_when_moving_down()
    def assert_not_skipping_floors(self,aCabin,aSignaledfloor):
        aCabin.assert_not_skipping_when_moving_down(aSignaledFloor)
    
    
class StoppedCabinState(CabinState):
    def is_moving_up(self):
        return False
    def is_moving_down(self):
        return False
    def is_stopped(self):
        return True
    def goto_moving_up(self,aCabin):
        aCabin.goto_moving_up_from_stopped()
    def goto_moving_down(self,aCabin):
        aCabin.goto_moving_down_from_stopped()
    def goto_stopped(self,aCabin):
        aCabin.goto_stopped_from_stopped()
    def open_command_issued(self,aCabin):
        aCabin.open_command_when_stopped()
    def assert_not_skipping_floors(self,aCabin,aSignaledFloor):
        aCabin.assert_not_skipping_when_stopped(aSignaledFloor)

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