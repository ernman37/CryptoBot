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
            else:
                return False

    #check if current coin is already in queue, if so, move to front
    def moveFront(self, coin):
        for count, x in enumerate(self.appendQue):
            if x == coin:
                self.appendQue.pop(count)
        self.appendQue.insert(0, coin)


    #append now item to que
    def appendQueue(self, coin):
        #check if it is already in queue, if so, move upfront
        if self.inQueue(coin):
            self.moveFront(coin)
            return True
        #otherwise, append to queue if it is not full
        elif self.isFull == False and self.checkValid(coin):
            self.queueArr.append(coin)
            #Successfull operatin
            return True
        #Unsuccessful append
        return False

    # Remove/consume element from queue
    def removeQueue(self):
        if not self.isEmpty:
            return self.appendQue.pop(0) 
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
        else:
            return False

    #check if current coint passed is 
    def checkValid(self, currentCoin):
        for x in self.bitArray:
            if x == currentCoin:
                return True
        return False

    def printCurrQueue(self):
        print(self.queueArr)
