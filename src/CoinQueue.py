import sys

class Queue:
    def __init__(self):
        self.bitArray = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'MATICUSDT', 'MANAUSDT']
        self.MAX_SIZE = 5
        self.queueArr = []

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

    #append now item to que
    def appendQueue(self, coin):
        #check if it is already in queue, if so, move upfront
        if self.inQueue(coin):
            self.moveFront(coin)
            print("Moving ", coin, " to Front of Queue!")
            return True
        #otherwise, append to queue if it is not full
        elif not self.isFull():
            self.queueArr.append(coin)
            print("Moved ", coin, " to Back of Queue!")
            #Successfull operatin
            return True
        #Unsuccessful append
        return False

    #Smaller names for functions for easier integration from other queue class 
    # another name to remove something from queue
    def get(self):
        self.removeQueue()

    # another name for append Queue
    def put(self, coin):
        self.appendQueue(coin)
    
    def empty(self):
        self.isEmpty()
    
    def full(self):
        self.isFull()

    # Remove/consume element from queue
    def removeQueue(self):
        if not self.isEmpty():
            return self.queueArr.pop(0) 
        else:
            print("Queue is Empty! Cannot get next coin!", file = sys.stderr)

    # Check if queue is empty 
    def isEmpty(self):
        return len(self.queueArr)  == 0

    #check if Queue is full
    def isFull(self):
        if len(self.queueArr) == self.MAX_SIZE:
            print("Que is full!")
            return True
        return False

    #check if current coint passed is 
    def checkValid(self, currentCoin):
        for x in self.bitArray:
            if x == currentCoin:
                return True
        return False

    def printCurrQueue(self):
        print(self.queueArr)

# TODO: Remove this main function later
def main():
    obj = Queue()
    obj.appendQueue(5)
    obj.appendQueue(10)
    obj.appendQueue(7)
    obj.printCurrQueue()
    obj.appendQueue(7)
    obj.appendQueue(8)
    obj.appendQueue(9)
    obj.removeQueue()
    obj.appendQueue(11)
    obj.printCurrQueue()
    obj.appendQueue(11)
    obj.printCurrQueue()

if __name__ == "__main__":
    main()

