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
    
class ElevatorController:

    CABIN_SENSORS_NOT_SYNCHRONIZED = "Sensor de cabina desincronizado"
    CABIN_DOOR_SENSORS_NOT_SYNCHRONIZED = "Sensor de puerta desincronizado"

    def __init__(self):
        self.elevatorState = "idle"
        self.cabin = Cabin()
        self.cabinCurrentFloor = 0
        self.calls = []
        self.waitingForPeople = False
        
    ## Observadores de estados ##  

    def isIdle(self):
        return self.elevatorState == "idle"

    def isWorking(self):
        return self.elevatorState == "working"

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
        return self.waitingForPeople

    
    ## Otros observadores ##

    def cabinFloorNumber(self):
        return self.cabinCurrentFloor 

    def isCabinGoingUp(self):
        return self.nextFloor() > self.cabinFloorNumber()

    def isCabinGoingDown(self):
        return self.nextFloor() < self.cabinFloorNumber() 
    
    def callsLeft(self):
        return len(self.calls) != 0

    def noCallsLeft(self):
        return not self.callsLeft()

    def nextFloor(self):
        if self.callsLeft():
            return self.calls[0]
        else: 
            return "No calls left"

    def isInQueue(self, aFloor):
        for floor_i in self.calls:
            if floor_i == aFloor :
                return True
        return False

    ## Chequeos para levantar excepciones

    def isCabinFalling(self, floor):
        return self.cabinFloorNumber() > floor and floor < self.nextFloor()

    def isCabingGoingInWrongDirection(self, floor):
        return self.isCabinFalling(floor) or (self.cabinFloorNumber() < floor and floor > self.nextFloor())
    
    def isCabinSkippingFloors(self, floor):
        return (self.isCabinGoingUp() and floor-1 != self.cabinFloorNumber()) or (self.isCabinGoingDown() and floor+1 != self.cabinFloorNumber())
    
    
    ## SENALES ##

    def cabinDoorClosed(self):
        #Este if es dudoso... ¿Tiene sentido que la puerta pueda tirar un ElevatorEmergency?
        #¿Deberían quizás llamarse ElevatorCabin y ElevatorCabinDoor?
        #¿O se podrá tirar un DoorException, agarrarla con catch y relanzarla...
        if self.isCabinDoorClosing():
            self.cabin.doorIsClosed()
            self.cabin.move()
        else:
            raise ElevatorEmergency(self.__class__.CABIN_DOOR_SENSORS_NOT_SYNCHRONIZED)

    def cabinDoorOpened(self):
        #Este if parece fácil de sacar con polimorfismo
        if self.noCallsLeft():
            self.elevatorState = "idle"
        
        self.cabin.doorIsOpened()

    def cabinOnFloor(self, floor):
        #Con double dispatch se debería poder sacar esto, teniendo estados como en los otros
        if self.isCabinMoving():
            assert(self.callsLeft())
            
            if self.isCabinSkippingFloors(floor) or self.isCabingGoingInWrongDirection(floor):
                raise ElevatorEmergency(self.__class__.CABIN_SENSORS_NOT_SYNCHRONIZED)
            else:
                self.updateCurrentFloor(floor)

                if floor == self.nextFloor() :
        
                    self.cabin.stop()
                    self.cabin.openCommandIssued()
                    self.waitForPeople()
                    self.calls.pop(0)  

        else:
            #Este no sé, creo que no se puede sacar... A menos que modelemos todos los pisos posibles...
            #Lo cuál me parece ridículo, onda, hacer una lista de pisos... No sé
            if not self.cabinFloorNumber() == floor:
                raise ElevatorEmergency(self.__class__.CABIN_SENSORS_NOT_SYNCHRONIZED)


    def waitForPeopleTimedOut(self):
        self.waitingForPeople = False

        if self.noCallsLeft() :
            self.elevatorState = "idle"
        
        else:
            self.closeCabinDoor()


    ## ACCIONES 
    
    def goUpPushedFromFloor(self, aFloor):
        #Esto creo que con estados se puede sacar...
        if self.isIdle():
            self.elevatorState = "working"
            self.cabin.closeCommandIssued()

        self.addCallFromFloor(aFloor)

    def openCabinDoor(self):
        if self.isCabinStopped():
            self.cabin.openCommandIssued()

    def closeCabinDoor(self):  
        if self.isCabinDoorOpened() and self.isWorking() :
            self.cabin.closeCommandIssued()
            if self.isCabinWaitingForPeople():
                self.waitingForPeople = False

    def updateCurrentFloor(self, floor):
        self.cabinCurrentFloor = floor

    def waitForPeople(self):
        self.waitingForPeople = True

    def addCallFromFloor(self, aFloor):
        if not self.isInQueue(aFloor) :

            if self.noCallsLeft(): 
                self.calls.append(aFloor)

            elif self.isCabinStopped() and self.cabinFloorNumber() == aFloor: #estoy parado en ese piso  
                if self.isCabinDoorClosing:
                    self.openCabinDoor()
    
            elif self.isCabinGoingDown():
                if aFloor < self.cabinFloorNumber():
                    self.decreasingOrderInsert(aFloor)
                else :
                    self.increasingOrderInsert(aFloor)

            elif self.isCabinGoingUp(): 
                if aFloor > self.cabinFloorNumber():
                    self.increasingOrderInsert(aFloor)
                else: 
                    self.decreasingOrderInsert(aFloor)

    def decreasingOrderInsert(self, aFloor):
        pos = 0
        while ( pos < len(self.calls) and self.calls[pos] > aFloor ):
            pos += 1
        self.calls.insert(pos, aFloor)           

    def increasingOrderInsert(self, aFloor):
        pos = 0
        while ( pos < len(self.calls) and self.calls[pos] < aFloor ):
            pos += 1
        self.calls.insert(pos, aFloor)

class ElevatorEmergency(Exception):
    
    def __init__(self, message):
        self.message = message


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