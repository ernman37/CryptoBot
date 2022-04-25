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
from config import account

def main():
    setLogger()
    trader = Trader(account['apiKey'], account['secret'])
    coins = ['SOLUSD', 'MATICUSD', 'MANAUSD', 'APEUSD', 'AMPUSD']
    cryptoBot = CryptoBot(coins, trader)
    #cryptoBot.start()
    CoinApi.getAllUSDTradeables()

if __name__ == "__main__":
    main()
