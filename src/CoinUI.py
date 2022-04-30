from tkinter import *
import time
from CoinApi import CoinApi
from Trader import Trader
from CryptoBot import CryptoBot
import os.path
import os
from log import setLogger

setLogger()
window = Tk()
window.geometry("700x400")
vscrollbar = Scrollbar(window)
c = Canvas(window, background="#D2D2D2", yscrollcommand=vscrollbar.set)

vscrollbar.config(command=c.yview)
vscrollbar.pack(side=LEFT, fill=Y)

f = Frame(c)
c.pack(side="left", fill="both")
c.create_window(0, 0, window=f, anchor="nw")


cryptos = CoinApi.getAllUSDTradeables()
selectedCryptos = []
selected = [False] * len(cryptos)
CryptoCopy = []
i = []
trader = -1

t = [0]
value = [0]

listbox = 0
money = 0
total = 0
wallet = 0
moneyInput = 0
INPUT = 0
checkStop = IntVar()
running = False
bot = 0

for k in range(len(selected)):
    i.append(IntVar())

def closing():
    global bot
    try: 
        exportData()
        bot.stop(True)
        window.destroy()
    except Exception as E:
        print(E)
    os._exit(0)

def exportData():
    plotFile = open("Graph.txt", "w")
    plotFile.write("X data:\n")
    for i in range(len(t)):
        plotFile.write(str(t[i])+", ")
    plotFile.write("\n")
    plotFile.write("Y data:\n")
    for i in range(len(value)):
        plotFile.write(str(value[i])+", ")
    plotFile.write("\n")


def begin():
    global selected, wallet, trader, moneyInput, INPUT, bot, stop, running
    timeSinceLast = time.time()
    selection()
    if INPUT != '' and not running:
        try: ##if there are no cryptos selected, do not run
            pos = selected.index(True)
        except:
            pos = -1
        if INPUT >= 12.50 and pos != -1: ##at least one crypto and at least $12.50 has to be entered to run
            if not os.path.exists("src/config.py"):
                exit(1)
            else:
                from config import account
                trader = Trader(account['apiKey'], account['secret'])
                if trader == 1 or trader == -1:
                    exit(1)
                else:
                    print(selectedCryptos)
                    wallet = trader.getPortfolioUSDBalance()
                    bot = CryptoBot(selectedCryptos, trader)
                    bot.start()
                    running = True
                    value.pop()
                    value.append(INPUT)
                    while running:
                        while time.time() - timeSinceLast < 30:
                            try:
                                window.after(1, window.update())
                            except:
                                pass
                        timeSinceLast = time.time()
                        wallet = trader.getPortfolioUSDBalance()
                        newVal = (trader.getPortfolioUSDBalance() - wallet) + value[len(value)-1]
                        value.append(newVal)
                        t.append(t[len(t)-1] + 30)

                        
def selection(): ##handle changes to money and checklist
    global i, listbox, money, selected, INPUT
    listbox.delete(0, END)
    temp = 0
    for k in range(len(i)):
        if i[k].get() == 1:
            if cryptos[k] in selectedCryptos:
                continue
            selectedCryptos.append(cryptos[k])
            selected[k] = True
            listbox.insert(END, selectedCryptos[-1])
    if (money.get() != ''):
        temp = int(money.get())
        INPUT = temp
    
def ownedCryptos():
    global listbox, money, stop, checkStop
    listbox = Listbox(window, width=20, height = 20)
    start = Button(window, text="Start", command=begin)
    stop = Button(window, text="Stop", command=closing)
    money = Entry(window)
    listbox.pack()
    money.pack()
    start.pack()
    stop.pack()

def checkboxes(): ##makes checkboxes and save button
    global CryptoCopy, i
    save = Button(window, text="Save selected", command=selection)
    save.pack()
    for k in range(len(cryptos)):
        Checkbutton(f, variable=i[k], text=cryptos[k]).pack()

if __name__ == "__main__":
    window.protocol("WM_DELETE_WINDOW", closing)
    checkboxes()
    ownedCryptos()
    window.update()
    c.config(scrollregion=c.bbox("all"))
    window.mainloop()