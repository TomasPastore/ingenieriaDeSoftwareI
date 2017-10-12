#For Python this file uses encoding: utf-8

import unittest
from elevatorcabindoor import ElevatorCabinDoor

#^ eso es provicional... En sí se me ocurre la opción de que el ElevatorController les pase la clase... Pero no sé

class ElevatorCabin(object):
    def __init__(self):
        self.MOVING_UP = MovingUpCabinState()
        self.MOVING_DOWN = MovingDownCabinState()
        self.STOPPED = StoppedCabinState()
        self._state = self.STOPPED
        self._door = ElevatorCabinDoor()
        self._currentFloor = 0

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
        self._door.open_button_pressed()

    def goto_moving_from_stopped(self):
        self._state = self.MOVING
    def goto_stopped_from_moving(self):
        self._state = self.STOPPED
    def goto_moving_from_moving(self):
        raise Exception("Already moving")
    def goto_stopped_from_stopped(self):
        raise Exception("Already stopped")

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

class MovingCabinState(CabinState):
    def is_moving(self):
        return True
    def is_stopped(self):
        return False
    def goto_moving(self,cabin):
        cabin.goto_moving_from_moving()
    def goto_stopped(self,cabin):
        cabin.goto_stopped_from_moving()


class StoppedCabinState(CabinState):
    def is_moving(self):
        return False
    def is_stopped(self):
        return True
    def goto_moving(self,cabin):
        cabin.goto_moving_from_stopped()
    def goto_stopped(self,cabin):
        cabin.goto_stopped_from_stopped()

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