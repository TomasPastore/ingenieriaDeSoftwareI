#This file uses encoding: utf-8
#
# Developed by 10Pines SRL
# License: 
# This work is licensed under the 
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. 
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ 
# or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, 
# California, 94041, USA.
#  
import unittest
from cabindoor import CabinDoor
from cabin import Cabin
from elevatoremergency import ElevatorEmergency
from pendingfloorsrecord import PendingFloorsRecord

    
class ElevatorController:

    def __init__(self):

        self.IDLE = IdleElevatorState()
        self.WORKING = WorkingElevatorState()

        self.elevatorState = self.IDLE

        self.cabin = ElevatorCabin()

        self.pendingFloors = PendingFloorsRecord()
        
    ## Observadores de estados ##  

    def isIdle(self):
        return self.elevatorState.isIdle()

    def isWorking(self):
        return self.elevatorState.isWorking()

    def isCabinStopped(self):
        return self.cabin.isStopped()

    def isCabinMoving(self):
        return self.cabin.isMoving()

    def isCabinDoorOpened(self):
        return self.cabin.isDoorOpened()

    def isCabinDoorOpening(self):
        return self.cabin.isDoorOpening()

    def isCabinDoorClosed(self):
        return self.cabin.isDoorClosed()

    def isCabinDoorClosing(self):
        return self.cabin.isDoorClosing()

    def isCabinWaitingForPeople(self):
        return self.cabin.isWaitingForPeople()
    
    ## Otros observadores ##

    def cabinFloorNumber(self):
        return self.cabin.currentFloor() 

    def isCabinGoingUp(self):
        return self.cabin.isGoingUp()

    def isCabinGoingDown(self):
        return self.cabin.isGoingDown() 
    

    def anyCallLeft(self):
        return self.pendingFloors.anyCallLeft()

    def noCallsLeft(self):
        return not self.anyCallLeft()

    def nextFloor(self):
        self.pendingFloors.nextFloor(self.cabin)

    ## SENALES ##

    def cabinDoorClosed(self):
        self.cabin.doorIsClosed()
        self.cabin.goToNextFloor(self.pendingFloors.nextFloor())

    def cabinDoorOpened(self):
        self.cabin.doorIsOpened()
        self.pendingFloors.doorIsOpened(self)

    def cabinOnFloor(self, floor):
        self.cabin.updateCurrentFloor(floor)
        self.cabin.stop()
        self.cabin.openCommandIssued()
        self.cabin.waitForPeople()
        self.pendingFloors.onFloor(floor)  

    def waitForPeopleTimedOut(self):
        self.cabin.waitForPeopleTimedOut()

        self.pendingFloors.waitForPeopleTimedOut(self)
        #Pasar a Idle en esto ^
        
        self.closeCabinDoor()

    ## ACCIONES 
    
    def goUpPushedFromFloor(self, aFloor):
        
        self.elevatorState.gotoWorking()

        self.addCallFromFloor(aFloor)

    def openCabinDoor(self):
        self.cabin.openCommandIssued()

    def closeCabinDoor(self):  
        self.elevatorState.closeCabinDoor(self)

    def closeCabinDoorWhenWorking():
        self.cabin.closeCommandIssued()


    def addCallFromFloor(self, aFloor):
        
        self.pendingFloors.addCallFromFloor(self, aFloor)
        
    def gotoWorkingFromIdle(self):
        self.cabin.closeCommandIssued()
        self.elevatorState = self.WORKING

    def gotoWorkingFromWorking(self):
        pass    

    def gotoIdleFromWorking(self):
        self.elevatorState = self.IDLE

    def gotoIdleFromIdle(self):
        pass    

class ElevatorState:

    def gotoWorking(self,anElevatorController):
        self.shouldBeImplementedBySubclass()
    def gotoIdle(self,anElevatorController):
        self.shouldBeImplementedBySubclass()
    def isWorking(self):
        self.shouldBeImplementedBySubclass()
    def isIdle(self):
        self.shouldBeImplementedBySubclass()
    def shouldBeImplementedBySubclass():
        raise NotImplementedError("Subclass responsibility")

class WorkingElevatorState(ElevatorState):

    def gotoWorking(self,anElevatorController):
        anElevatorController.gotoWorkingFromWorking()
    def gotoIdle(self,anElevatorController):
        anElevatorController.gotoIdleFromWorking()
    def closeCabinDoor(self,anElevatorController):
        anElevatorController.closeCabinDoorWhenWorking()
    def isWorking(self):
        return True
    def isIdle(self):
        return False

class IdleElevatorState(ElevatorState):

    def gotoWorking(self,anElevatorController):
        anElevatorController.gotoWorkingFromIdle()
    def gotoIdle(self,anElevatorController):
        anElevatorController.gotoIdleFromIdle()
    def isWorking(self):
        return False
    def isIdle(self):
        return True


class ElevatorTest(unittest.TestCase):

    def test01ElevatorStartsIdleWithDoorOpenOnFloorZero(self):
        elevatorController = ElevatorController()
        
        self.assertTrue(elevatorController.isIdle())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpened())
        self.assertEqual(0,elevatorController.cabinFloorNumber())
    
    def test02CabinDoorStartsClosingWhenElevatorGetsCalled(self):
        elevatorController = ElevatorController()
    
        elevatorController.goUpPushedFromFloor(1)
        
        self.assertFalse(elevatorController.isIdle())
        self.assertTrue(elevatorController.isWorking())
        
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertFalse(elevatorController.isCabinMoving())
        
        self.assertFalse(elevatorController.isCabinDoorOpened())
        self.assertFalse(elevatorController.isCabinDoorOpening())
        self.assertTrue(elevatorController.isCabinDoorClosing())
        self.assertFalse(elevatorController.isCabinDoorClosed())
    
    def test03CabinStartsMovingWhenDoorGetsClosed(self):
        elevatorController = ElevatorController()
    
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        
        self.assertFalse(elevatorController.isIdle())
        self.assertTrue(elevatorController.isWorking())
    
        self.assertFalse(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinMoving())
        
        self.assertFalse(elevatorController.isCabinDoorOpened())
        self.assertFalse(elevatorController.isCabinDoorOpening())
        self.assertFalse(elevatorController.isCabinDoorClosing())
        self.assertTrue(elevatorController.isCabinDoorClosed())
    
    def test04CabinStopsAndStartsOpeningDoorWhenGetsToDestination(self):
        elevatorController = ElevatorController()
    
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)

        self.assertFalse(elevatorController.isIdle())
        self.assertTrue(elevatorController.isWorking())
        
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertFalse(elevatorController.isCabinMoving())
                
        self.assertFalse(elevatorController.isCabinDoorOpened())
        self.assertTrue(elevatorController.isCabinDoorOpening())
        self.assertFalse(elevatorController.isCabinDoorClosing())
        self.assertFalse(elevatorController.isCabinDoorClosed())

        self.assertEquals(1,elevatorController.cabinFloorNumber())
        
    def test05ElevatorGetsIdleWhenDoorGetOpened(self):
        elevatorController = ElevatorController()
    
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        elevatorController.cabinDoorOpened()
        
        self.assertTrue(elevatorController.isIdle())
        self.assertFalse(elevatorController.isWorking())
        
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertFalse(elevatorController.isCabinMoving())

        self.assertTrue(elevatorController.isCabinDoorOpened())
        self.assertFalse(elevatorController.isCabinDoorOpening())
        self.assertFalse(elevatorController.isCabinDoorClosing())
        self.assertFalse(elevatorController.isCabinDoorClosed())
        
        self.assertEquals(1,elevatorController.cabinFloorNumber())
    
    # STOP HERE!
    
    def test06DoorKeepsOpenedWhenOpeningIsRequested(self):
        elevatorController = ElevatorController()
        
        self.assertTrue(elevatorController.isCabinDoorOpened())
        
        elevatorController.openCabinDoor()

        self.assertTrue(elevatorController.isCabinDoorOpened())
        
    def test07DoorMustBeOpenedWhenCabinIsStoppedAndClosingDoors(self):
        elevatorController = ElevatorController()
    
        elevatorController.goUpPushedFromFloor(1)
        
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorClosing())
        
        elevatorController.openCabinDoor()
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())
    

    def test08CanNotOpenDoorWhenCabinIsMoving(self):
        elevatorController = ElevatorController()
    
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinMoving())
        self.assertTrue(elevatorController.isCabinDoorClosed())

        elevatorController.openCabinDoor()
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinMoving())
        self.assertTrue(elevatorController.isCabinDoorClosed())
    

    def test09DoorKeepsOpeneingWhenItIsOpeneing(self):
        elevatorController = ElevatorController()
    
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())

        elevatorController.openCabinDoor()
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())
    

    # STOP HERE!!
    
    def test10RequestToGoUpAreEnqueueWhenRequestedWhenCabinIsMoving(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorOpened()
    
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinWaitingForPeople())
        self.assertTrue(elevatorController.isCabinDoorOpened())
    

    def test11CabinDoorStartClosingAfterWaitingForPeople(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorOpened()
        elevatorController.waitForPeopleTimedOut()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorClosing())
    

    def test12StopsWaitingForPeopleIfCloseDoorIsPressed(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorOpened()
    
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinWaitingForPeople())
        self.assertTrue(elevatorController.isCabinDoorOpened())

        elevatorController.closeCabinDoor()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorClosing())

    

    def test13CloseDoorDoesNothingIfIdle(self):
        elevatorController = ElevatorController()
        
        elevatorController.closeCabinDoor()

        self.assertTrue(elevatorController.isIdle())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpened())

    

    def test14CloseDoorDoesNothingWhenCabinIsMoving(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
    
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinMoving())
        self.assertTrue(elevatorController.isCabinDoorClosed())

        elevatorController.closeCabinDoor()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinMoving())
        self.assertTrue(elevatorController.isCabinDoorClosed())
    

    def test15CloseDoorDoesNothingWhenOpeningTheDoorToWaitForPeople(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
    
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())

        elevatorController.closeCabinDoor()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())


    # STOP HERE!!

    def test16ElevatorHasToEnterEmergencyIfStoppedAndOtherFloorSensorTurnsOn(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        try:
            elevatorController.cabinOnFloor(0)
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de cabina desincronizado")

    def test17ElevatorHasToEnterEmergencyIfFalling(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        try:
            elevatorController.cabinOnFloor(0)
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de cabina desincronizado")
        
    

    def test18ElevatorHasToEnterEmergencyIfJumpsFloors(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(3)
        elevatorController.cabinDoorClosed()
        try:
            elevatorController.cabinOnFloor(3)
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de cabina desincronizado")
        
    

    def test19ElevatorHasToEnterEmergencyIfDoorClosesAutomatically(self):
        elevatorController = ElevatorController()
        
        try:
            elevatorController.cabinDoorClosed()
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de puerta desincronizado")
        
    

    def test20ElevatorHasToEnterEmergencyIfDoorClosedSensorTurnsOnWhenClosed(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        try:
            elevatorController.cabinDoorClosed()
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de puerta desincronizado")
        

    def test21ElevatorHasToEnterEmergencyIfDoorClosesWhenOpening(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        try:
            elevatorController.cabinDoorClosed()
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de puerta desincronizado")
        
    

    # STOP HERE!!
    # More tests here to verify bad sensor function
    
    def test22CabinHasToStopOnTheFloorsOnItsWay(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinOnFloor(1)

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())
    
    
    def test23ElevatorCompletesAllTheRequests(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinOnFloor(1)
        elevatorController.cabinDoorOpened()
        elevatorController.waitForPeopleTimedOut()
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(2)
        
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())
    
    
    def test24CabinHasToStopOnFloorsOnItsWayNoMatterHowTheyWellCalled(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorClosed()
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinOnFloor(1)
        
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())
    
    
    def test25CabinHasToStopAndWaitForPeopleOnFloorsOnItsWayNoMatterHowTheyWellCalled(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorClosed()
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinOnFloor(1)
        elevatorController.cabinDoorOpened()
        elevatorController.waitForPeopleTimedOut()
        
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorClosing())
    

if __name__ == '__main__':
    unittest.main()