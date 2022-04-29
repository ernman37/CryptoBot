import sys
import logging
from threading import Lock

class Queue:
    def __init__(self, maxSize):
        self.log = logging.getLogger()
        try:
            self.MAX_SIZE = maxSize
            self.queueArr = []
            self.lock = Lock()
        except Exception as e:
            self.log.error("Error setting up Queue")

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
                returnValue = True
            #otherwise, append to queue if it is not full
            elif not self.full():
                self.queueArr.append(coin)
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
        value = None
        try:
            if not self.empty():
                value = self.queueArr.pop(0) 
        finally:
           self.lock.release()
        return value
            
    # Check if queue is empty 
    def empty(self):
        return len(self.queueArr)  == 0

    def isFull(self):
        return self.full()

    #check if Queue is full
    def full(self):
        if len(self.queueArr) == self.MAX_SIZE:
            print("Que is full!")
            return True
        return False
