
class PendingFloorsRecord():

    def __init__(self):
        self._record = [] 

    def nextFloor(self):
        if self._record:
            return self._record[0]

    def addCallFromFloor(self,anElevatorController,aFloor):
        #Este no sabemos como sacarlo porque si lo implementamos con un bitmap no podemos
        #saber next floor en estado stopped
        if not aFloor in self._record:
            
            #Este if no es del dominio del problema
            if anElevatorController.cabinFloorNumber() == aFloor:
                anElevatorController.openCabinDoor()

            else: 
                order = anElevatorController.howShouldIAdd(self,aFloor)
                #No es del dominio del problema,se puede sacar subclasificando una clase "order"
                
                if order == "INCREASING_ORDER":
                    self.increasingOrderInsert(aFloor)
                elif order == "DECREASING_ORDER":
                    self.decreasingOrderInsert(aFloor)
                else:
                    raise Exception("Unknown order") 
    
    def onFloor(self, anElevatorController, aFloor):
        if aFloor == self.nextFloor():
            anElevatorController.arrivedToNextFloorSignal()
            self._record.pop(0)
    def doorIsOpened(self,anElevatorController):
        if not self._record:
                anElevatorController.gotoIdle()      

    def waitForPeopleTimedOut(self,anElevatorController):
        #Se puede sacar con un null object que no llegamos a implementar
        if not self._record:
            anElevatorController.gotoIdle()

    def decreasingOrderInsert(self, aFloor):
        pos = 0
        while ( pos < len(self._record) and self._record[pos] > aFloor ):
            pos += 1
        self._record.insert(pos, aFloor)           

    def increasingOrderInsert(self, aFloor):
        pos = 0
        while ( pos < len(self._record) and self._record[pos] < aFloor ):
            pos += 1
        self._record.insert(pos, aFloor)
