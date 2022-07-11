'''
    File: log.py
    Creator: Ernest M Duckworth IV
    Created: Sunday Apr 17 2022 at 01:45:53 AM
    For: CryptoBot
    Description: Sets the logger for the entire project so that we have streamlined stdout and logfile format and writing
'''
import logging, sys

def setLogger():
    logFormat = "%(threadName)s - %(asctime)s - %(message)s"
    logger = logging.getLogger()
    fileHandler = logging.FileHandler("../reports/log/logfile.log")
    streamHandler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(logFormat, "%H:%M:%S")
    streamHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)
    return logger