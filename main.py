import tkinter
from tkinter import *
from tkinter import filedialog
import checkCam
import json
import JSONadvanced
import os
import numpy as np
import cv2
import time
import threading
import client
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


print(os.getcwd()) # shows correct path

# the window structure


window = Tk()
window.geometry("400x600")
window.minsize(400, 600)
window.maxsize(400, 600)
window.title("HorstFX Thesis Project")
#window.configure(background='grey')


logo = PhotoImage(file="horstLogo.png")
window.iconphoto(True, logo)

menu_back = PhotoImage(file="buttons/Thws-logo_English.png").subsample(4, 4) # copy of HorstFX Main Menu
background = Label(window, image=menu_back)
background.pack(side="bottom") # the image has to be properly aligned not sure why "y" doesnt work

# the window controls



slider_value_text = StringVar()
slider_value_text.set("Robot Speed")


c = client.Client()



stop_execution = False  # flags stop/pause/resume

pause_event = threading.Event()
pause_event.set()

mlt = 1 # speed multiplier

anch_x = 0.530 #used
anch_y = -0.050 #used
pick_x = 0.330 #notYet
pick_y = 0.250 #notYet

anch_x_label = StringVar()
anch_x_label.set(anch_x)

json_name = 'complexPallete.json'
horst_program = 'StackingProgram.js'

"""global stop_execution
    if stop_execution:
        return
    global pause_event
    pause_event.wait()"""""


def start_click_connect_thread():
    connect_thread = threading.Thread(target=clickConnect)
    connect_thread.start()

def readJSON(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data

def stop_execution_click():
    button2.configure(state=DISABLED)
    global pause_event
    global stop_execution
    if pause_event.is_set():
        stop_execution = True
        print("User stopped the execution.")
    else:
        stop_execution = True
        print("User stopped the execution when program was on pause.")
        pause_event.set()



def pause_execution():
    global pause_event
    if pause_event.is_set():
        pause_event.clear()  # Clear to PAUSE
        button2.configure(text="Resume")
    else:
        pause_event.set()  # Set to RESUME
        button2.configure(text="Pause")


def checkPauseStop():
    global stop_execution
    if stop_execution:
        return True
    global pause_event
    pause_event.wait()
    return False

def update_speed(value):
    global mlt
    mlt = float(value)
    print(mlt)
    slider_value_text.set(f"Robot speed: {mlt*100}%")

"""def readJSON(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)"""

def aboveObject(jspath, dx, dy):
    if checkPauseStop():
        return
    c.moveJoint(dx + 0.330 + jspath['dim_x']/2, 0.250 - jspath['dim_y']/2 - dy, 0.16043 + jspath['dim_z'], -0.00000,
                -0.00000, 1.00000, -0.00000, 1.0 * mlt)

def toTheObject(jspath, dx, dy):
    if checkPauseStop():
        return
    c.moveLinear(dx + 0.330 + jspath['dim_x']/2, 0.250 - jspath['dim_y']/2 - dy, 0.00231 + jspath['dim_z'], -0.00000, -0.00000, 1.00000, -0.00000, 0.65 * mlt)

def liftObject(jspath, dx, dy):
    if checkPauseStop():
        return
    #gripCheck()
    c.moveLinear(dx + 0.330 + jspath['dim_x']/2, 0.250 - jspath['dim_y']/2 - dy, 0.17043 + jspath['dim_z'],
                -0.00000, -0.00000, 1.00000, -0.00000, 1.0 * mlt)

def aboveApproach(jspath, anch_x, anch_y):
    if checkPauseStop():
        return

    c.moveJoint(anch_x + jspath['x'] + jspath['dim_x'] / 2, anch_y - jspath['y'] - jspath['dim_y'] / 2,
                0.05 + jspath['z'] + jspath['dim_z'] + 0.1,
                -0.00000, -0.00000, 1.00000, -0.00000, 0.75 * mlt)

def performApproach(jspath, approach_function, anch_x, anch_y):
    if checkPauseStop():
        return
    approach_function(jspath, anch_x, anch_y)

def clickConnect():
    button2.configure(text="Pause", state=ACTIVE)
    global stop_execution
    stop_execution = False
    data = readJSON(json_name)  # JSON file name given in the beginnning

    for pallet in data["pallets"]:
        amount = len(pallet["boxes"])
        print(amount)

    dx = 0.05
    dy = 0
    gripInit()
    for i in range(amount):
        if stop_execution:
            break

        jspath = data["pallets"][0]["boxes"][i]

        if dx > 0.4:
            print("Here")
            print(dx)
            dx = 0.05
            dy = data["pallets"][0]["boxes"][0]['dim_y']
            print(dy)

        aboveObject(jspath, dx, dy) # be ready
        toTheObject(jspath, dx, dy) # go down linear and slow
        gripSuck()
        liftObject(jspath, dx, dy) # go up also linear

        dx += jspath['dim_x']
        print(c.getCurrentRobotPositionV())

        approachFunction = getApproachFunc(jspath['approach']) #get number
        performApproach(jspath, approachFunction, anch_x, anch_y) #do function linked to that number

        aboveApproach(jspath, anch_x, anch_y) # when object is released, go up for secure height




def getApproachFunc(approach_number):
    approachMap = {
        "1": approach1,
        "3": approach3,
        "5": approach5,
        "7": approach7,
        "9": approach9
    }
    return approachMap[approach_number]

def approach1(jspath, anch_x, anch_y):
    if checkPauseStop():
        return
    #gripCheck()
    print(jspath["z"])

    c.moveJoint(anch_x + jspath['x'] + jspath['dim_x']/2, anch_y - jspath['y'] - jspath['dim_y']/2,
                0.15 + jspath['z'] + jspath['dim_z'] + 0.03,
                -0.00000, -0.00000, 1.00000, -0.00000, 1.0 * mlt)
    approachFinal(jspath)

def approach3(jspath, anch_x, anch_y):
    if checkPauseStop():
        return
    #gripCheck()
    print(jspath["z"])

    c.moveJoint(anch_x + jspath['x'] + jspath['dim_x']/2 + 0.05, anch_y - jspath['y'] - jspath['dim_y']/2 + 0.05,
                0.15 + jspath['z'] + jspath['dim_z'] + 0.03,
                -0.00000, -0.00000, 1.00000, -0.00000, 1.0 * mlt)
    approach32(jspath, anch_x, anch_y)

def approach32(jspath, anch_x, anch_y):
    if checkPauseStop():
        return
    #gripCheck()
    c.moveJoint(anch_x + jspath['x'] + jspath['dim_x'] / 2 + 0.05, anch_y - jspath['y'] - jspath['dim_y'] / 2 + 0.05,
                0.053 + jspath['z'] + jspath['dim_z'],
                -0.00000, -0.00000, 1.00000, -0.00000, 1.0 * mlt)
    approachFinal(jspath, anch_x, anch_y)

def approach5(jspath, anch_x, anch_y):
    if checkPauseStop():
        return
    #gripCheck()
    print(jspath["z"])

    c.moveJoint(anch_x + jspath['x'] + jspath['dim_x']/2 + 0.05, anch_y - jspath['y'] - jspath['dim_y']/2 - 0.05,
                0.15 + jspath['z'] + jspath['dim_z'] + 0.03,
                -0.00000, -0.00000, 1.00000, -0.00000, 1.0 * mlt)
    approach52(jspath, anch_x, anch_y)

def approach52(jspath, anch_x, anch_y):
    if checkPauseStop():
        return
    #gripCheck()
    c.moveJoint(anch_x + jspath['x'] + jspath['dim_x'] / 2 + 0.05, anch_y - jspath['y'] - jspath['dim_y'] / 2 - 0.05,
                0.053 + jspath['z'] + jspath['dim_z'],
                -0.00000, -0.00000, 1.00000, -0.00000, 1.0 * mlt)
    approachFinal(jspath, anch_x, anch_y)

def approach7(jspath, anch_x, anch_y):
    if checkPauseStop():
        return
    #gripCheck()
    print(jspath["z"])

    c.moveJoint(anch_x + jspath['x'] + jspath['dim_x']/2 - 0.05, anch_y - jspath['y'] - jspath['dim_y']/2 - 0.05,
                0.15 + jspath['z'] + jspath['dim_z'] + 0.03,
                -0.00000, -0.00000, 1.00000, -0.00000, 1.0 * mlt)
    approach72(jspath, anch_x, anch_y)

def approach72(jspath, anch_x, anch_y):
    if checkPauseStop():
        return
    #gripCheck()
    c.moveJoint(anch_x + jspath['x'] + jspath['dim_x'] / 2 - 0.05, anch_y - jspath['y'] - jspath['dim_y'] / 2 - 0.05,
                0.053 + jspath['z'] + jspath['dim_z'],
                -0.00000, -0.00000, 1.00000, -0.00000, 1.0 * mlt)
    approachFinal(jspath, anch_x, anch_y)

def approach9(jspath, anch_x, anch_y):
    if checkPauseStop():
        return
    #gripCheck()
    print(jspath["z"])

    c.moveJoint(anch_x + jspath['x'] + jspath['dim_x']/2 - 0.05, anch_y - jspath['y'] - jspath['dim_y']/2 + 0.05,
                0.15 + jspath['z'] + jspath['dim_z'] + 0.03,
                -0.00000, -0.00000, 1.00000, -0.00000, 1.0 * mlt)
    approach92(jspath, anch_x, anch_y)

def approach92(jspath, anch_x, anch_y):
    if checkPauseStop():
        return
    #gripCheck()
    c.moveJoint(anch_x + jspath['x'] + jspath['dim_x'] / 2 - 0.05, anch_y - jspath['y'] - jspath['dim_y'] / 2 + 0.05,
                0.053 + jspath['z'] + jspath['dim_z'],
                -0.00000, -0.00000, 1.00000, -0.00000, 1.0 * mlt)
    approachFinal(jspath, anch_x, anch_y)

def approachFinal(jspath, anch_x, anch_y):
    if checkPauseStop():
        return
    c.moveJoint(anch_x + jspath['x'] + jspath['dim_x'] / 2, anch_y - jspath['y'] - jspath['dim_y'] / 2,
                0.053 + jspath['z'] + jspath['dim_z'],
                -0.00000, -0.00000, 1.00000, -0.00000, 0.5 * mlt)

    gripRele()
    print(f"Approach {jspath['approach']} performed")
    print(c.getCurrentRobotPositionV())



def approachSpec(jspath,z_stack, anch_x, anch_y):
    print(jspath["z"])

    c.moveJoint(anch_x + jspath['dim_x']/2, anch_y - jspath['dim_y']/2,
                0.15 + z_stack + jspath['dim_z'] + 0.03,
                -0.00000, -0.00000, 1.00000, -0.00000, 1.0)

    c.moveJoint(anch_x + jspath['dim_x']/2, anch_y - jspath['dim_y']/2,
                0.05 + z_stack + jspath['dim_z'],
                -0.00000, -0.00000, 1.00000, -0.00000, 1.0)

    gripRele()
    print("ApproachSpec performed")

    c.moveJoint(anch_x + jspath['dim_x'] / 2, anch_y - jspath['dim_y'] / 2,
                0.15 + z_stack + jspath['dim_z'] + 0.03,
                -0.00000, -0.00000, 1.00000, -0.00000, 1.0)





def clickOpenWindow():
    def save_values(): # function to change some initial values of anchor points
        anch_x = entry1.get()
        anch_y = entry2.get()
        print("Values entered: "+ anch_x + " " + anch_y)
        new_window.destroy()

    new_window = Toplevel(window)
    new_window.title("Enter Values")

    label1 = Label(new_window, text="Please enter an x-coordinate for Palette Anchor point:")
    label1.pack(pady=5)
    entry1 = Entry(new_window)
    entry1.insert(0, "0.530")
    entry1.pack(pady=5)

    label2 = Label(new_window, text="Please enter an y-coordinate for Palette Anchor point:")
    label2.pack(pady=5)
    entry2 = Entry(new_window)
    entry2.insert(0, "-0.05")
    entry2.pack(pady=5)

    label3 = Label(new_window, text="Please enter the height at which you want to drop boxes:")
    label3.pack(pady=5)
    entry3 = Entry(new_window)
    entry3.insert(0, "0.05")
    entry3.pack(pady=5)

    save_button = Button(new_window, text="Save", command=save_values)
    save_button.pack(pady=5)


def clickRunJSprog():

    data = readJSON(json_name)  # JSON func

    for pallet in data["pallets"]:
        amount = str(len(pallet["boxes"]))
        print(amount)  # not needed, test


    file_path = horst_program  # open StackingProgram.js
    with open(file_path, 'r') as file:
        horstfx_js = file.read() #initiate long str


    boxes_data = []
    for pallet in data['pallets']:
        for box in pallet['boxes']:
            boxes_data.append({
                'dim_x': box['dim_x'],
                'dim_y': box['dim_y'],
                'dim_z': box['dim_z'],
                'x': box['x'],
                'y': box['y'],
                'z': box['z'],
                'approach': box['approach']
            })

    # Convert the list of dictionaries to a JSON string
    jsonize = json.dumps(boxes_data)
    print(jsonize)

    horstfx_js = horstfx_js.replace("PUTHERE", jsonize).replace("BOXES", amount)
    print(horstfx_js)


    v = 0 #CHANGE
    if v == 0:
        c.switchActivity(1) # go to Program mode
        time.sleep(1)
        c.setGlobalSpeed(0.75)
        c.execute(horstfx_js)


    print("Done.")
    safetyStatus = c.safetyStatus()
    print(safetyStatus)
    programName = c.programName()
    print(programName)


def clickPause():
    pause_execution()
    """if client.Client().isRunning() == True:
        client.Client().pause()
    else:
        client.Client().proceed()
    #client.Client().moveJoint(0, 0, 0, 0, 0, 0, 0, 0.5)"""

def clickStop():
    stop_execution_click()

def clickLoad():
    data = readJSON(json_name)

    pal_numbero = 0
    pallet = data["pallets"][pal_numbero]
    pal_x = pallet["width"]
    pal_y = pallet["length"]

    print("X dimension of a pallet: " + str(pal_x))
    print("Y dimension of a pallet: " + str(pal_y))

    for pallet in data["pallets"]:
        amount = len(pallet["boxes"])
        print("There are " + str(amount) + " boxes")

    for i in range(amount):

        jspath = data["pallets"][0]["boxes"][i]



    def determineX(pal_x, jspath):
        midpoint = pal_x / 2.0
        if jspath['x'] < midpoint:
            x_loc = 1
        else:
            x_loc = 0

    def determineY(pal_y, jspath):
        midpoint = pal_x / 2.0
        if jspath['y'] < midpoint:
            y_loc = 1
        else:
            y_loc = 0

    def firstApproach(x_loc, y_loc):
        if x_loc == 1 & y_loc == 1:
            apr = 9
        elif x_loc == 1 & y_loc == 0:
            apr = 3
        elif x_loc == 0 & y_loc == 1:
            apr = 7
        else:
            apr = 5
        return apr




    #checkCam.checkCamera()
    """if client.Client().isRunning() == True:
        client.Client().abort()
        print("Abort")
    else:
        client.Client().play()
        print("Start the program")
    #JSONadvanced.advanced()"""

def clickCamera():
    checkCam.checkCamera()


def clickExit():
    window.destroy()

def gripInit():
    c.setOutput("TOOL_OUTPUT_1", 0)
    time.sleep(0.2)
    c.setOutput("TOOL_OUTPUT_2", 0)

def gripSuck():
    global stop_execution
    if stop_execution:
        return
    global pause_event
    pause_event.wait()
    c.setOutput("TOOL_OUTPUT_1", 1)
    time.sleep(0.5)
    c.setOutput("TOOL_OUTPUT_1", 0)
    print("Gripper takes")

def gripRele():
    global stop_execution
    if stop_execution:
        return
    global pause_event
    pause_event.wait()
    c.setOutput("TOOL_OUTPUT_2", 1)
    time.sleep(0.3)
    c.setOutput("TOOL_OUTPUT_2", 0)
    print("Gripper releases")

def gripCheck():
    while c.getInput("TOOL_INPUT_1") != 1:
        c.setOutput("TOOL_OUTPUT_1", 1)
    c.setOutput("TOOL_OUTPUT_1", 0)



button1 = Button(window, text="START", command=start_click_connect_thread, state=ACTIVE)
button1.pack(side="top", pady=5)
button2 = Button(window, text="Pause", command=clickPause, state=DISABLED)
button2.pack(side="top", pady=5)
button3 = Button(window, text="Stop", command=clickStop, state=ACTIVE)
button3.pack(side="top", pady=5)
button4 = Button(window, text="Start JS file", command=clickRunJSprog, state=ACTIVE)
button4.pack(side="top", pady=5)
button5 = Button(window, text="Options and tuning", command=clickOpenWindow, state=ACTIVE)
button5.pack(side="top", pady=5)
button6 = Button(window, text="Load", command=clickLoad, state=ACTIVE)
button6.pack(side="top", pady=5)
button7 = Button(window, text="Camera", command=clickCamera, state=ACTIVE)
button7.pack(side="top", pady=5)
buttonExit = Button(window, text="EXIT", command=clickExit, state=ACTIVE)
buttonExit.pack(side="top", pady=5)

speed_multiplier_slider = Scale(window, from_=0.1, to=1, orient=HORIZONTAL, resolution=0.05, command=update_speed)
speed_multiplier_slider.set(1)
speed_multiplier_slider.pack(side="left", padx=20)

slider_value_label = Label(window, textvariable=slider_value_text, fg="black", font=("Calibri", 14))
slider_value_label.pack(side="right", padx=30)

anch_x_label = Label(window, textvariable=anch_x, fg="black", font=("Calibri", 11))
anch_x_label.pack(side="top", pady=10)



window.mainloop()

