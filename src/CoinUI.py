from ast import Global
from turtle import color
import dearpygui.dearpygui as dpg
import time
import numpy as np
from CoinApi import CoinApi
from log import setLogger
from Trader import Trader
from CryptoBot import CryptoBot
import os.path

Running = False

crypto = CoinApi.getAllUSDTradeables()
selected = [False]*len(crypto)
ownedCryptos = []
total = 0

trader = -1
t = [0]
value = [0]
timeSinceLast = 0

def close():
    dpg.delete_item("pop")

def receiveInputButton(sender, data): ##handle input from buttons and checkboxes
    global Running
    global selected
    global timeSinceLast
    global total
    pos = 0
    if sender == "Start":##Start
        timeSinceLast = time.time()
        total = dpg.get_value("total")
        try: ##if there are no cryptos selected, do not run
            pos = selected.index(True)
        except:
            pos = -1
        if total >= 12.50 and pos != -1: ##at least one crypto and at least $12.50 has to be entered to run
            if not os.path.exists("config.py"):
                #missConf()
                Running = True
                while Running:
                    renderGraph()
                ##kill all threads, sell, etc
            else:
                from config import account
                setLogger()
                trader = Trader(account['apikey'], account['secret'])
                #bot = CryptoBot(ownedCryptos, trader)
                ##bot.start()
                Running = True
                while Running:
                    renderGraph()
        else:
            popup()
    elif sender == "Stop": ##Stop
        Running = False
    elif sender == "pick": ##color picker
        dpg.configure_item("line", color = data)

def setRunning(bool):
    global Running
    Running = bool

def getTrader():
    return trader

def receiveInput(sender, data): ##handle input from checkboxes and total money
    global Running
    if sender == "total":
        value.clear()
        value.append(data)
    else: ##checkboxes
        if Running == False:
            dpg.delete_item("Owned")
            ownedCryptos.clear() ##we will be recreating this based on each selection, so deletion is enabled
            selected[crypto.index(sender)] = data
            for i in range(len(crypto)):
                if selected[i] == True:
                    ownedCryptos.append(crypto[i])
            selectedCryptos()
        else:
            runningPop()

def getRunning():
    global Running
    return Running

def renderGraph(): ##rerender the graph with new data every 30 seconds
    global timeSinceLast
    global Running
    resetGraph()
    resetOptions()
    resetCrypto()
    while time.time() - timeSinceLast < 30:
        dpg.render_dearpygui_frame() ##The last thing to do is poll for stop press
    timeSinceLast = time.time()
    

def popup():
    dpg.add_window(label="WARNING", tag="pop", modal=True, on_close=close)
    if not ownedCryptos and dpg.get_value("total") < 12.50:
        dpg.add_text(parent="pop", default_value="You must select one or more cryptos and have $12.50 to invest")
    elif dpg.get_value("total") < 12.50:
        dpg.add_text(parent="pop", default_value="You must have at least $12.50 to invest")
    elif not ownedCryptos:
        dpg.add_text(parent="pop", default_value="You must select one or more cryptos")

def runningPop():
    dpg.add_window(label="WARNING", tag="pop", modal=True, on_close=close)
    dpg.add_text(parent="pop", default_value="You cannot change settings after pressing start")

def missConf():
    dpg.add_window(label="WARNING", tag="pop", modal=True, on_close=close)
    dpg.add_text(parent="pop", default_value="Missing config file, required to start trading")

def selectedCryptos():
    with dpg.window(label="Selected Cryptos", height=1000, width = 220, pos=[600, 0], tag="Owned"): ##currently purchased cryptos
        dpg.add_listbox(items=ownedCryptos, num_items=55, width=200, tag="list")

def tradableCryptos():
    global Running
    global selected
    with dpg.window(label="All Cryptos", width=220, height = 1000, pos=[820, 0], tag="Tradable"): ##checkbox for all cryptos
        for i in range(len(crypto)):
            dpg.add_checkbox(label=crypto[i], default_value=selected[i], tag=crypto[i], callback=receiveInput)

def graph():
    global t, value
    t.append(t[len(t)-1]+30)
    value.append(time.time())
    if getTrader() != -1:
        pass
        #value.append(Trader.getPortfolioUSDBalance(getTrader()))
    with dpg.window(label="Graph", width=600, height=400, tag="Plot"):
        with dpg.plot(label="Overall performance", width=600, height=400, tag="perf"):
            dpg.add_plot_axis(dpg.mvXAxis, label = "time (seconds)", tag="x_axis")
            dpg.add_plot_axis(dpg.mvYAxis, label="Value (USD)", tag ="y_axis")
            dpg.add_line_series(t, value, parent="y_axis", tag = "line")

def options():
    global Running
    global total
    with dpg.window(label="Options", width=600, height=200, pos=[0, 400], tag="Options"): ##input window
        if Running == False:
            dpg.add_input_float(label="Total Money", tag="total", default_value = total, callback=receiveInput)
            dpg.add_button(label="Start", tag="Start", callback=receiveInputButton)
            dpg.add_button(label="Stop", tag = "Stop", callback=receiveInputButton)
        else:
            dpg.add_input_float(label="Total Money", tag="total", default_value = total, callback=runningPop)
            dpg.add_button(label="Start", tag="Start", callback=runningPop)
            dpg.add_button(label="Stop", tag = "Stop", callback=receiveInputButton)

def colorPicker():
    global Running
    with dpg.window(label="Graph Color", width=600, height=400, pos=[0, 600], tag="Picker"): ##color picker
        if Running == False:
            dpg.add_color_picker(display_hex=True, tag="pick", callback=receiveInputButton)
        else:
            dpg.add_color_picker(display_hex=True, tag="pick", callback=runningPop)


def resetGraph():
    dpg.delete_item("line")
    dpg.delete_item("y_axis")
    dpg.delete_item("x_axis")
    dpg.delete_item("perf")
    dpg.delete_item("Plot")
    graph()

def resetOptions():
    dpg.delete_item("total")
    dpg.delete_item("Start")
    dpg.delete_item("Stop")
    dpg.delete_item("Options")
    options()

def resetSelected():
    global selected
    dpg.delete_item("list")
    dpg.delete_item("Owned")
    selectedCryptos()

def resetCrypto():
    for i in crypto:
        try:
            dpg.delete_item(i)
        except:
            pass
    dpg.delete_item("Tradable")
    tradableCryptos()
    resetSelected()
    dpg.render_dearpygui_frame()

def resetPicker():
    dpg.delete_item("pick")
    dpg.delete_item("Picker")
    colorPicker()

def resetAll():
    resetOptions()
    resetSelected()
    resetCrypto()

def menuBar():
    dpg.add_window(label="menu", tag="window", no_close=True, no_title_bar=True, height = 300, width=300, pos = [1040, 0])
    dpg.add_button(parent="window", label="Graph", callback=resetGraph)
    dpg.add_button(parent="window", label="Options", callback=resetOptions)
    dpg.add_button(parent="window", label="Selected Cryptos", callback=resetSelected)
    dpg.add_button(parent="window", label="All Cryptos", callback=resetCrypto)
    dpg.add_button(parent="window", label="Color Picker", callback=resetPicker)
    dpg.add_button(parent="window", label="Style Editor", callback=dpg.show_style_editor)
    

if __name__ == "__main__":
    #create space and initialize dpg
    dpg.create_context()
    dpg.create_viewport(title='CryptoBot', width=1940, height=1050) ##create outer window
    viewPos = [0, 0]
    dpg.set_viewport_pos(viewPos)
    #start creating windows and widgets
    selectedCryptos()
    graph()
    options()
    colorPicker()
    menuBar()
    tradableCryptos()

    #finishing touches for dpg
    dpg.setup_dearpygui()
    dpg.show_viewport()
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
    Running = False
    dpg.destroy_context()
    ##sell all crypto, kill all threads, maybe export the graph?