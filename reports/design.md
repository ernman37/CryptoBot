<!--
    File: design.md
    Creator: Ernest M Duckworth IV
    Created: Monday Feb 21 2022 at 11:35:55 AM
    For: CryptoBot
    Description: Design file for the Crypto Bot
--->
# CryptoBot

## Hardware Details

### Hardware List

- Raspberry Pi 4 (4gbs)($150-200)
   - Internet connection
   - Display capabilities (HTML)
- Sensor(s)
   - Laser Fingerprint scanner (~$20)
   - Additional PI Components
   - Raspberry Pi case ($40-90)
   - Raspberry Pi fan ($10-20)
   - Arduino (Optional $10)
   - Tools/setup kit ($20-50)
   - Comes with most raspberry pi kits
- Required Additional Components
   - Power Source
   - Ethernet Cable
   - Display (personal is fine for now)

### Hardware Explanation

- Raspberry PI 4 (4gs)
   - The Raspberry PI 4 with 4 gigs of ram is our best option
   - 4 cores for our multi-threading
   - 4gs of ram (allow us a larger data set per coin)
   - Easy integration for sensors
      - Fingerprint Scanner
- Fingerprint Scanner
   - The fingerprint scanner returns a hash value for every person's fingerprint
   - This allows us to encrypt everyone's data with a different hash value
   - This way the only person who can see encrypted data is the person with the fingerprint
      - Allow us to store sensitive data locally
- Additional kits
   - Fan for keeping the PI as cool as it can while running the program
   - Kit to keep PI safe so the group does not have to buy multiple through the time frame of the project
   - Arduino if we choose to add different scanners

## Software Details

### Threads

#### Main

- On entry, it will make a user sign in or create an account
   - Creating an account will require the user to either enter their coin base API keys or skip entering their information and run paper trading only
- From here they can select a list of coins they are interested in
   - Have a default list for easy access
      - Can filter information out of the default list
   - Can add their own coins
      - We will have to add a test to ensure user-entered coins exist 
- Now Reader can be created with their selected Coins 
   - Trading style can be determined as well (paper trading or coin base)
- From here the main process will wait for keyboard arguments from *client*
   - Keyboard arguments could be
      - Account details
         - Total in account
         - Total in various coins
         - Possible percentage data depending on API capabilities
      - Certain coin information display
         - Display coin in the various time frames (1m,5m,10m,30m,1h, etc)
         - Display coin with indicators
      - Display top watch
         - Coins with the highest `Analyzer` rating
      - Quit/SignOut
         - Close the threads and exit the program
      - switcher
         - Switch to new user 
         - Signout && sign-in
      - Etc

#### Reader

- The bot will scrub the current market fetching new candles for selected **Coins** as they are released
   - Fetches are grabbed by their timestamp
      - In the case of a fetch failure
         - Wait and try to connect after a small amount of time
         - Keep running count of consecutive failed fetches
            - If it reaches over 5 in a row end program with an error
   - This is done in a forever process(single thread dedicated to running this process alone)
   - Will be done sequential loading with all coins
      - Coins will not be loaded concurrently (on multiple threads)
   - Once all coins have been downloaded the reader will execute the `Analyzer`
      - And go back to trying to fetch new candle data
   - Maintain the `dataFrame` size, don't allow any coin to have over x amount of candle info 

#### Analyzer
- Will be created by `Reader`
- On entry, it will begin analyzing the data of all the coins in the data stream
- Algorithm
   - Use various trading strategies to create a weight for if a coin should be bought or not
   - Can be on various strategies
      - Indicators
         - RSI/MACD/etc
      - Speculative 
         - support/resistance
      - Etc
   - As weights are determined keep a sorted list of which coins have the highest weights
   - Depending on strategy
      - Create a thread to execute buy orders on hit cases
      - Wait until the end of the analyzer to create a single thread that executes multiple buy orders
         - In this case we could not create a second thread and just pass the process into a buy/series series where it executes a query of buy/sells
            - On each successful buy/sell another thread could be created for `Notifier`
- Close thread and return control back to `Reader`

#### Buyer

- Will be created by `Analyzer`
- On entry, it will begin 
   - A: Executing a single order
   - B: Executing a handful of orders
- Determine which platform is being used
   - `Coinbase` 
   - `PaperTrader`
- Execute the trades
- Close thread and return back to `Analyzer`

#### Notifier(optional)

- Will be created by `Analyzer` after successful execution of `Buyer`
- Connects to the discord server
- Prints buy/sell the message
- Returns control back to `Analyzer`

### Further Details

#### Thread Status

- The max amount of threads that this program may be running at a single time will be **4**
- Most of the time it will only be running **2**
- Since the `Main` will have to communicate with `Reader` for a lot of its processes
- There will have to be a 2-way communication process between the 2 so that `Main` can request information from `Reader` and `Reader` can return the requested information
- `Reader` will not necessarily need communication between the buyer just be able to tell if it returned with a success or failure message(determine if buy/sell was successful)
- `Main` will have to be able to access its own API to the market so data can be fetched for the user(does not come out of our backend unless the client wants the same candlesticks that are used in the backend **1m** by default)
- `Notifier` could be sending out multiple notifications to multiple different platforms if possible

### Libraries:
- Pandas (DataFrames)
- Pandas-TA (technical analyisis)
- CCXT (coin API)
- Dearpy.gui (GUI)
