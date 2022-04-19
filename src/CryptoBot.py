'''
    File: CryptoBot.py
    Creator: Ernest M Duckworth IV
    Created: Monday Feb 28 2022 at 03:43:19 PM
    For: Crypto Bot
    Description: A crypto trading bot for either paper trading or actual market trading
'''
from CoinsScanner import CoinsScanner
from Analyzer import Analyzer
from Trader import Trader
import queue
import threading
import logging
import sys
from log import *

class CryptoBot: 

    def __init__(self, coins, trader: Trader, timeFrame='1m'): 
        self.log = logging.getLogger()
        self.log.error("Setting up Crypto Bot")
        self.coins = coins
        self.trader = trader
        scannerAnalyzerQueue = queue.Queue(len(coins))
        self.scanner = CoinsScanner(coins, scannerAnalyzerQueue, timeFrame)
        self.analyzer = Analyzer(self.scanner.coins, scannerAnalyzerQueue, self.trader.tradeQueue)

    def start(self):
        self.log.error("Starting Crypto Bot")
        self.scannerThread = threading.Thread(target=self.scanner.scanForever, name="Scanner")
        self.traderThread = threading.Thread(target=self.trader.tradeForever, name="Trader")
        self.analyzerThread = threading.Thread(target=self.analyzer.analyzeForever, name="Analyzer")
        self.scannerThread.start()
        self.analyzerThread.start()
        self.traderThread.start()