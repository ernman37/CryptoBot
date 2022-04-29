#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from subprocess import call

class FingerPrint:

    def __init__(self):
        self.scanner = self.initializeSensor()

    def run(self):
        if self.scanner.getTemplateCount() == 0:
            self.loopForNewFinger()
        else:
            ans = ""
            while not ans in ['1', '2', '3']:
                ans = input("1: Login Existing User \n2: Create New User (must have existing user) \n3: exit\nEnter Option: ")
            if ans == '1':
                self.loopForEnrolledFinger()
            elif ans == '2':
                print("Scan pre-existing Finger to Add new one")
                time.sleep(1)
                self.loopForEnrolledFinger()
                time.sleep(1)
                self.loopForNewFinger()
            else:
                exit(0)

    def initializeSensor(self):
        try:
            sensor = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
            if ( sensor.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')
            return sensor
        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            return False

    def enrollNewFinger(self):
        try:
            print("Enrolling New Finger")
            self.scanFinger()
            result = self.scanner.searchTemplate()
            positionNumber = result[0]
            if ( positionNumber >= 0 ):
                print('Template already exists at position #' + str(positionNumber))
                return False
            print('Remove finger...')
            time.sleep(1)
            print('Waiting for same finger again...')
            self.scanFinger(0x02)
            if not self.fingersMatch():
                print('Fingers do not match')
                return False
            self.scanner.createTemplate()
            positionNumber = self.scanner.storeTemplate()
            print('Finger enrolled successfully!')
            print('New template position #' + str(positionNumber))
        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            return False
        return True

    def loopForNewFinger(self):
        while not self.enrollNewFinger():
            print("Please Try again")
            time.sleep(1)

    def scanEnrolledFinger(self):
        self.scanFinger()
        return self.foundFinger()

    def loopForEnrolledFinger(self):
        while not self.scanEnrolledFinger():
            print("Please Try again")
            time.sleep(1)

    def scanFinger(self, buff=0x01):
        print("Place Finger on Scanner...")
        while not self.scanner.readImage():
            pass
        self.scanner.convertImage(buff)

    def foundFinger(self):
        result = self.scanner.searchTemplate()
        position = result[0]
        if not position >= 0:
            print("Finger is not Stored")
            return False
        print("Finger was Found")
        return True

    def fingersMatch(self):
        return not self.scanner.compareCharacteristics() == 0
        
if __name__ == "__main__":
    fingerScanner = FingerPrint()
    fingerScanner.run()

