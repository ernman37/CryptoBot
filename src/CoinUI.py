from tkinter import *
import time
from CoinApi import CoinApi
from Trader import Trader
from CryptoBot import CryptoBot
import os.path

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

for k in range(len(selected)):
    i.append(IntVar())

def closing():
    exportData()
    print("FDSHJ")
    window.destroy()
    ##Kill threads and sell

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
    global selected, wallet, trader, moneyInput, INPUT
    timeSinceLast = time.time()
    if INPUT != '':
        try: ##if there are no cryptos selected, do not run
            pos = selected.index(True)
        except:
            pos = -1
        print(type(INPUT))
        if INPUT >= 12.50 and pos != -1: ##at least one crypto and at least $12.50 has to be entered to run
            if not os.path.exists("config.py"):
                exit(1)
            else:
                from config import account
                trader = Trader(account['apiKey'], account['secret'])
                if trader == 1 or trader == -1:
                    exit(1)
                else:
                    wallet = trader.getPortfolioUSDBalance()
                    bot = CryptoBot(ownedCryptos, trader)
                    bot.start()
                    value.pop()
                    value.append(moneyInput)
                    while True:
                        while time.time() - timeSinceLast < 30:
                            pass
                        wallet = trader.getPortfolioUSDBalance()
                        value.append((trader.getPortfolioUSDBalance() - wallet) + value[len(value)-1])
                        t.append(t[len(t)-1] + 30)

                        
def selection(): ##handle changes to money and checklist
    global i, listbox, money, selected, INPUT
    listbox.delete(0, END)
    temp = 0
    for k in range(len(i)):
        if i[k].get() == 1:
            selectedCryptos.append(cryptos[k])
            selected[k] = True
            listbox.insert(END, selectedCryptos.pop())
    if (money.get() != ''):
        temp = int(money.get())
        INPUT = temp
    

def ownedCryptos():
    global listbox, money
    listbox = Listbox(window, width=20, height = 58)
    start = Button(window, text="Start", command=begin)
    money = Entry(window)
    listbox.pack()
    money.pack()
    start.pack()

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