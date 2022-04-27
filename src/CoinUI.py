import dearpygui.dearpygui as dpg
import time
import numpy as np
from CoinApi import CoinApi

Running = False
crypto = CoinApi.getAllUSDTradeables()
selected = [False]*len(crypto)
ownedCryptos = []
liquid = []

def close():
    dpg.delete_item("pop")

def receiveInputButton(sender, data): ##handle input from buttons and checkboxes
    pos = 0
    if sender == "Start":##Start
        try: ##if there are no cryptos selected, do not run
            pos = selected.index(True)
        except:
            pos = -1
        if float(dpg.get_value("total")) >= 12.50 and pos != -1: ##at least one crypto and at least $12.50 has to be entered to run
            if pos != -1:
                Running = True
                while True:
                    renderGraph()
        else:
            popup()
    elif sender == "Stop": ##Stop
        Running = False
    elif sender == "pick": ##color picker
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_PlotLines, data, category=dpg.mvThemeCat_Plots) ##The values I'm recieving for data aren't appropriate for themes
                dpg.bind_theme(global_theme)


def receiveInput(sender, data): ##handle input from checkboxes
    dpg.delete_item("Owned")
    ownedCryptos.clear() ##we will be recreating this based on each selection, so deletion is enabled
    selected[crypto.index(sender)] = data
    for i in range(len(crypto)):
        if selected[i] == True:
            ownedCryptos.append(crypto[i])
    selectedCryptos()


def renderGraph(): ##rerender the graph with updated data every frame
    dpg.delete_item("Plot")
    graph()
    dpg.render_dearpygui_frame() ##at some point this will have to be checking if stop has been clicked

def renderFrame(): ##stable renderer before clicking run
    dpg.render_dearpygui_frame()

def popup():
    dpg.add_window(label="WARNING", tag="pop", modal=True, on_close=close)
    if not ownedCryptos and dpg.get_value("total") < 12.50:
        dpg.add_text(parent="pop", default_value="You must select one or more cryptos and have $12.50 to invest")
    elif dpg.get_value("total") < 12.50:
        dpg.add_text(parent="pop", default_value="You must have at least $12.50 to invest")
    elif not ownedCryptos:
        dpg.add_text(parent="pop", default_value="You must select one or more cryptos")

def selectedCryptos():
    with dpg.window(label="Selected Cryptos", height=1000, width = 220, pos=[600, 0], tag="Owned"): ##currently purchased cryptos
        dpg.add_listbox(items=ownedCryptos, num_items=55, width=200)

def tradableCryptos():
    with dpg.window(label="All Cryptos", width=220, height = 1000, pos=[820, 0], tag="Tradable"): ##checkbox for all cryptos
        for i in range(len(crypto)):
            dpg.add_checkbox(label=crypto[i], tag=crypto[i], callback=receiveInput)

def graph():
    liquid.append(time.time()) 
    with dpg.window(label="Graph", width=600, height=400, tag="Plot"):
        dpg.add_simple_plot(default_value=liquid, height=350, width=600)

def options():
    with dpg.window(label="Options", width=600, height=200, pos=[0, 400], tag="Options"): ##input window
        dpg.add_input_float(label="Total Money", tag="total")
        dpg.add_button(label="Start", tag="Start", callback=receiveInputButton)
        dpg.add_button(label="Stop", tag = "Stop", callback=receiveInputButton)

def colorPicker():
    with dpg.window(label="Graph Color", width=600, height=400, pos=[0, 600], tag="Picker"): ##color picker
        dpg.add_color_picker(display_rgb=True, tag="pick", callback=receiveInputButton)


def resetGraph():
    dpg.delete_item("Plot")
    graph()

def resetOptions():
    dpg.delete_item("Options")
    options()

def resetSelected():
    dpg.delete_item("Owned")
    ownedCryptos.clear()
    for i in range(len(selected)):
        selected[i] = False
    selectedCryptos()

def resetCrypto():
    dpg.delete_item("Tradable")
    tradableCryptos()
    print(ownedCryptos)
    resetSelected()
    dpg.render_dearpygui_frame()

def resetPicker():
    dpg.delete_item("Picker")
    colorPicker()


def menuBar():
    dpg.add_window(label="menu", tag="window", no_close=True, no_title_bar=True, height = 300, width=300, pos = [1040, 0])
    dpg.add_button(parent="window", label="Graph", callback=resetGraph)
    dpg.add_button(parent="window", label="Options", callback=resetOptions)
    dpg.add_button(parent="window", label="Selected Cryptos", callback=resetSelected)
    dpg.add_button(parent="window", label="All Cryptos", callback=resetCrypto)
    dpg.add_button(parent="window", label="Color Picker", callback=resetPicker)
    

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
    while Running == False:
        renderFrame()
 
    dpg.destroy_context()