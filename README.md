# CryptoBot

Raspberry Pi Crypto Bot

### Details

- Simple Crypto Trading bot built for use on Raspberry Pi's 
- Trades on **BinanceUS**
- Requires user to create a `config.py` with account API keys
- Uses Fingerprint Scanner to allow bot to be started 
- Allows for multiple fingers/people to be allowed to start the bot

### config.py

- config.py should contain a map `account`
- Should be exactly like this...
```
account = {
    apiKey: "Your API key",
    secret: "Your Secret key"
}
```

### Usage

- Create `config.py` and place it in the `src/` directory
- `pip install -r requirements.txt` so that you have all the needed libraries for this project
- navigate to `bin/`
  - run `./run.sh` to begin the program
- Follow the fingerprint instructions/options 
- GUI will pull up with list of coins that can be selected 
  - Money to trade also has to be inputted below 
  - Hitting save selected after inputting Money to trade and selecting coins to trade will allow you to press the `start` button
- Clicking `start`
  - calls `CryptoBot.start()` and begins trading on the selected coins forever
- Clicking `stop` 
  - calls `CryptoBot.stop()` and sells out of current positions and ends the program


### Contributions

Ernest Duckworth IV (ernman37):
- Analyzer.py
- CoinAPI.py
- CoinData.py
- CoinsScanner.py
- CryptoBot.py
- FingerPrint.py
- log.py
- main.py
- Trader.py

Sam McKay (retrope13):
- CoinUI.py
- Grapher.py

Sammy White (SammyWhite000):
- CoinQueue.py