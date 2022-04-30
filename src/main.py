'''
    File: main.py
    Creator: Ernest M Duckworth IV
    Created: Monday Feb 21 2022 at 11:49:27 AM
    For: Crypto Bot
    Description: Main driver for the bot
'''
import pandas as pd
import time
from CoinData import CoinData
from CoinApi import CoinApi
from CoinsScanner import CoinsScanner
from Trader import Trader
from CryptoBot import CryptoBot
from log import setLogger
from FingerPrint import FingerPrint
import os.path, os, sys
import time

log = setLogger()

def main():
    account = findConfig()
    tryFingerScanner()
    os.system("python3 CoinUI.py")
    #trader = Trader(account['apiKey'], account['secret'])
    #coins = ['BTCUSD', 'SOLUSD', 'MATICUSD', 'MANAUSD', 'ADAUSD', 'LTCUSD', 'XLMUSD']
    #cryptoBot = CryptoBot(coins, trader)
    #cryptoBot.start()
    while True:
        time.sleep(1)

def tryFingerScanner():
    try:
        fingerScanner = FingerPrint()
        fingerScanner.run()
    except Exception as E:
        ans = ""
        while ans not in ['1', '2']:
            ans = input("1: Run without authorization\n2: exit\nEnter Option: ")
        if ans == '2':
            exit(1)
        log.error("Trying to Run without authorization")

def findConfig():
    if os.path.exists('config.py'):
        from config import account
        log.error("Found config File")
        return account
    else:
        log.error("Cannot Find Config file cannot begin without it")
        exit(1)

 
if __name__ == "__main__":
    main()
