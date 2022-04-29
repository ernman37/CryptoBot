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
from CoinQueue import Queue
import threading, logging, sys, time

class CryptoBot: 
    def __init__(self, coins, trader, timeFrame='1m'): 
        self.log = logging.getLogger()
        self.log.error("Setting up Crypto Bot")
        self.coins = coins
        self.trader = trader
        scannerAnalyzerQueue = Queue(len(coins))
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
        return True

    def stop(self, forceStop=False):
        self.log.error("Starting shutdown for CryptoBot")
        if forceStop:
            self.trader.hardExit()
        else:
            self.trader.setTrading(False)
            while self.traderThread.is_alive():
                time.sleep(1)
        self.traderThread.join()
        self.log.error("Shut Down Trader")
        self.analyzer.doneAnalyzing = True
        self.scanner.doneScanning = True
        self.analyzerThread.join()
        self.log.error("Shut Down Analyzer")
        self.scannerThread.join()
        self.log.error("Shut Down Scanner")
        self.log.error("Successfully Shut Down Crypto Bot")
        return True
