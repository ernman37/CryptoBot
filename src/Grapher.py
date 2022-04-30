import dearpygui.dearpygui as dpg

charBuff = []
t = [0]
value = [0]

def graph():
    global t, value
    print(value)
    print(t)
    dpg.add_window(label="Graph", width=870, height=600, no_title_bar=True, no_resize=True, tag="window")
    dpg.add_plot(label="Overall performance", width=870, height=500, tag="plot", parent="window")
    dpg.add_plot_axis(dpg.mvXAxis, label = "time (seconds)", tag="x_axis", parent="plot")
    dpg.add_plot_axis(dpg.mvYAxis, label="Value (USD)", tag="y_axis", parent="plot")
    dpg.add_line_series(t, value, parent="y_axis")

def readData():
    global t, value
    file1 = open("Graph.txt", "r")
    file1.readline()
    t.pop()
    value.pop()
    temp = 0
    for line in file1:
        for word in line.split():
            num = word
            if not num:
                break
            else:
                charBuff.append(num)
    
    for i in range(len(charBuff)):
        if charBuff[i] == ", ":
            charBuff.pop(i)
            pass
        elif charBuff[i] == "Y":
            charBuff.pop(i)
            break
        else:
            temp = int(charBuff[i].replace(",",""))
            t.append(temp)
    
    print(charBuff)
    for i in range(len(charBuff)):
        try:
            temp = int(charBuff[i].replace(",", ""))
            pos = t.index(temp)
        except:
            pos = -1
        if charBuff[i] == ", ":
            pass
        elif charBuff[i] == "data:":
            pass
        elif pos == -1:
            temp = float(charBuff[i].replace(",", ""))
            value.append(temp)

if __name__ == "__main__":
    dpg.create_context()
    dpg.create_viewport(title="Graph", width=885, height=550, resizable=False)
    viewPos = [0, 0]
    dpg.set_viewport_pos(viewPos)

    readData()
    graph()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()