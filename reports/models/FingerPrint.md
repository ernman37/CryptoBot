<!--
    File: FingerPrint.md
    Creator: Ernest M Duckworth IV
    Created: Friday Apr 29 2022 at 05:51:09 PM
    For: CryptoBot
    Description: FingerPrint model Documentation 
--->
# FingerPrint 

### Members

- scanner: `<PyFingerprint>`

#### Libraries

- time
- pyfingerprint
- subprocess

#### Methods

- Constructor()
   - Tries to initialize scanner
     - exits if it fails

- run()
  - If there are no fingers register on scanner asks user to scan finger 
  - if there are fingers registered
    - asks if they want to login existing user
      - Will scan until it recognizes finger
    - asks if they want to add new user
      - Will need pre-existing user to add new user
        - Scan pre-existing user
      - Will now ask to scan new user
    - asks if they want to exit
      - exits the program

- initializeSensor()
  - initalizes the sensor for constructor

- enrollNewFinger()
  - Tries to enroll new finger
  - if fails exits

- loopForNewFinger()
  - while enrollNewFinger() fails keep trying to scan new finger

- scanEnrolledFinger()
  - Scans for enrolled finger
  - returns bool on if found or not

- scanFinger()
  - Process for scanning the finger

- foundFinger()
  - tests if it has found the finger that was recently scanned 

- fingersMatch()
  - test to make sure that fingers that were being enrolled match each other
