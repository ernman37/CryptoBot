'''
    File: log.py
    Creator: Ernest M Duckworth IV
    Created: Sunday Apr 17 2022 at 01:45:53 AM
    For: 
    Description:
'''
import logging, sys

def setLogger():
    logFormat = "%(threadName)s - %(message)s"
    logger = logging.getLogger()
    fileHandler = logging.FileHandler("logfile.log")
    streamHandler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(logFormat)
    streamHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)
    return logger