import sys
from threading import Lock

class Queue:
    def __init__(self):
        try:
            self.bitArray = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'MATICUSDT', 'MANAUSDT']
            self.MAX_SIZE = 5
            self.queueArr = []
            self.lock = Lock()
        except Exception as e:
            self.log("Error setting up Queue")

    #check if current coin is in queue already
    def inQueue(self, coin):
        for x in self.queueArr:
            if x == coin:
                return True
        return False

    #if coin is already in queue, move it to the front
    def moveFront(self, coin):
        for count, x in enumerate(self.queueArr):
            if x == coin:
                self.queueArr.pop(count)
                self.queueArr.insert(0, coin)

    #append now item to cue; Lock function 
    def put(self, coin):
        self.lock.acquire()
        #check if it is already in queue, if so, move upfront
        returnValue = False
        try:
            if self.inQueue(coin):
                self.moveFront(coin)
                print("Moving ", coin, " to Front of Queue!")
                returnValue = True
            #otherwise, append to queue if it is not full
            elif not self.full():
                self.queueArr.append(coin)
                print("Moved ", coin, " to Back of Queue!")
                #Successfull operatin
                returnValue = True
        finally:
            self.lock.release()
        #Unsuccessful append
        return returnValue

    #Smaller names for functions for easier integration from other queue class 
    # another name to remove something from queue
    # Remove/consume element from queue
    def get(self):
        self.lock.acquire()
        if not self.empty():
            self.lock.release()
            return self.queueArr.pop(0) 
        else:
            print("Queue is Empty! Cannot get next coin!", file = sys.stderr)
            self.lock.release()
            
    # Check if queue is empty 
    def empty(self):
        return len(self.queueArr)  == 0

    #check if Queue is full
    def full(self):
        if len(self.queueArr) == self.MAX_SIZE:
            print("Que is full!")
            return True
        return False

    def printCurrQueue(self):
        print(self.queueArr)

# TODO: Remove this main function later
def main():
    obj = Queue()
    obj.put(5)
    obj.put(10)
    obj.put(7)
    obj.printCurrQueue()
    obj.put(7)
    obj.printCurrQueue()
    obj.put(8)
    obj.put(9)
    obj.printCurrQueue()
    obj.put(11)
    obj.printCurrQueue()
    obj.get()
    obj.printCurrQueue()

if __name__ == "__main__":
    main()

