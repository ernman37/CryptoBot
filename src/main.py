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
import os.path
import time

log = setLogger()

if os.path.exists('config.py'):
    from config import account
else:
    log.error("Cannot Find Config file cannot begin without it")
    exit(1)

def main():
    fingerScanner = FingerPrint()
    fingerScanner.run()
    trader = Trader(account['apiKey'], account['secret'])
    coins = ['BTCUSD', 'SOLUSD', 'MATICUSD', 'MANAUSD', 'ADAUSD', 'LTCUSD', 'XLMUSD']
    cryptoBot = CryptoBot(coins, trader)
    cryptoBot.start()
    #time.sleep(3)
    #cryptoBot.stop()
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
