# potentiometer_plot.py

import serial
import time

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from infi.systray import SysTrayIcon
import math

import os
import json
import sys

from pynput.keyboard import Key, Controller

import threading

keyboard = Controller()
run = True

try:
    dataPath = os.path.expanduser('~/Documents/SliderX')
    print("Folder Found")
    try:
        f = open(dataPath + "/Settings.json")
        json_file = dataPath + "/Settings.json"
        data = json.load(f)
        #print(data)
        Com_Port = data["COM_PORT"]
        Flip_Pots = data["flip"]
        POT1_Json = data["POT1"]
        POT2_Json = data["POT2"]
        POT3_Json = data["POT3"]
        POT4_Json = data["POT4"]
        print(Com_Port)
        print(Flip_Pots)
        print(POT1_Json)
        print(POT2_Json)
        print(POT3_Json)
        print(POT4_Json)
    except:
        print("Error Loading File")
except:
    print("Folder not Found")

initial_modification_time = os.path.getmtime(json_file)
def check_json_for_updates():
    global initial_modification_time
    while True:
        current_modification_time = os.path.getmtime(json_file)
        if current_modification_time > initial_modification_time:
            # The file has been updated, do something here
            print('The JSON file has been updated!')
            # Update the initial modification time
            initial_modification_time = current_modification_time
            os.execv(sys.executable, ['python'] + sys.argv)
        time.sleep(5)

thread = threading.Thread(target=check_json_for_updates)
thread.start()

try:
    ser = serial.Serial(Com_Port, 9600, timeout=1)
except:
    print("ERROR! COULDNT CONNECT! RETRYING IN 10 SEC")
    time.sleep(10)
    try:
        ser = serial.Serial(Com_Port, 9600, timeout=1)
    except:
        print("ERROR! COULDNT CONNECT! RETRYING IN 10 SEC")
        time.sleep(10)
        try:
            ser = serial.Serial(Com_Port, 9600, timeout=1)
        except:
            print("ERROR! COULDNT CONNECT!")
            ser = serial.Serial(Com_Port, 9600, timeout=1)
            run = False
time.sleep(2) # who doesnt need a good sleep once in a while


def on_quit_callback(systray):
    global run
    run = False

def restart(systray):
    os.execv(sys.executable, ['python'] + sys.argv)

menu_options = (("Restart", None, restart),)
systray = SysTrayIcon("icon.ico", "SliderX by Itay Ayollo", menu_options, on_quit=on_quit_callback)
systray.start()

POT1_Json =  POT1_Json.replace(" ", "")
pot1List = POT1_Json.split(",")# list of applications.

POT2_Json =  POT2_Json.replace(" ", "")
pot2List = POT2_Json.split(",")# list of applications.

POT3_Json =  POT3_Json.replace(" ", "")
pot3List = POT3_Json.split(",")# list of applications.

POT4_Json =  POT4_Json.replace(" ", "")
pot4List = POT4_Json.split(",")# list of applications.

potentiometer1 = pot1List # what program to control.
potentiometer2 = pot2List # what program to control.
potentiometer3 = pot3List # what program to control.
potentiometer4 = pot4List # what program to control.

old_poten1 = -1.0 # for checking if the value changed later on
old_poten2 = -1.0 # for checking if the value changed later on
old_poten3 = -1.0 # for checking if the value changed later on
old_poten4 = -1.0 # for checking if the value changed later on

invert_pots = Flip_Pots

tolorence = 0.005 # the potentiometer values jump and move slightly so i use a little tolorence to combat that so that i only send change volume commands when actually moving the potentiometer.

max_pots_value = 4095 # the maximum value the current board outputs. Use 1023 for arduino boards and 4095 for ESP32 boards.

while (run):
    line = ser.readline()  # read a byte string
    if line:
        string = line.decode()  # convert the byte string to a unicode string
        #print(string)
        items = string.split('~') # split the string into seperate variables in a list using the "~" seperator that is in between the values in the string.

        num1 = int(items[0])  # convert the unicode string to an int
        num2 = int(items[1])  # convert the unicode string to an int
        num3 = int(items[2])  # convert the unicode string to an int
        num4 = int(items[3])  # convert the unicode string to an int

        volume1 = ((num1 - 0) / (max_pots_value - 0)) # Normalize values between 0 and 1
        volume2 = ((num2 - 0) / (max_pots_value - 0)) # Normalize values between 0 and 1
        volume3 = ((num3 - 0) / (max_pots_value - 0)) # Normalize values between 0 and 1
        volume4 = ((num4 - 0) / (max_pots_value - 0)) # Normalize values between 0 and 1

        if invert_pots:
            volume1 = 1 - volume1 # invert potentiometer values if true
            volume2 = 1 - volume2 # invert potentiometer values if true
            volume3 = 1 - volume3 # invert potentiometer values if true
            volume4 = 1 - volume4 # invert potentiometer values if true

        poten1 = volume1 # for checking if the value changed later on
        poten2 = volume2 # for checking if the value changed later on
        poten3 = volume3 # for checking if the value changed later on
        poten4 = volume4 # for checking if the value changed later on
        
        volume1 = f'{volume1:.2f}' # shorten the float to 2 digits after the decimal point. i dont need more than that.
        volume1 = float(volume1)
        #print(volume1)
        
        volume2 = f'{volume2:.2f}' # shorten the float to 2 digits after the decimal point.
        volume2 = float(volume2)
        #print(volume2)
        
        volume3 = f'{volume3:.3f}' # shorten the float to 2 digits after the decimal point.
        volume3 = float(volume3)
        #print(volume3)
        
        volume4 = f'{volume4:.4f}' # shorten the float to 2 digits after the decimal point.
        volume4 = float(volume4)
        #print(volume4)
        
        abc1 = volume1 + 0.001  #
        abc1 = abc1 - 0.001     #
                                #
        abc2 = volume2 + 0.001  #
        abc2 = abc2 - 0.001     #
                                #   for some reason python wont recognize my float as a float so this just jogs its memory i guess.
        abc3 = volume3 + 0.001  #
        abc3 = abc3 - 0.001     #
                                #
        abc4 = volume4 + 0.001  #
        abc4 = abc4 - 0.001     #

        
    pos1 = int(volume1 * 10)
    pos2 = int(volume2 * 10)
    pos3 = int(volume3 * 10)
    pos4 = int(volume4 * 10)
    
    print(pos1,",", pos2,",", pos3,",", pos4)
    systray.update(hover_text="SliderX                      by Itay Ayollo   ["+str(pos1)+","+str(pos2)+","+str(pos3)+","+str(pos4)+"]")

    pos1 = 10 - pos1
    pos2 = 10 - pos2
    pos3 = 10 - pos3
    pos4 = 10 - pos4

    i = 1
    


    if ( poten1 - old_poten1 > tolorence or  old_poten1 - poten1 > tolorence): # check if the current potentiometer value is diffrent than the last saved one while also taking the tolorence into account.
        sessions1 = AudioUtilities.GetAllSessions()
        for session in sessions1:
            volume1 = session._ctl.QueryInterface(ISimpleAudioVolume)
            for app in pot1List:
                if session.Process and session.Process.name() == app: # check if an application with that name is currently running.
                    volume1.SetMasterVolume(abc1, None) # change the volume.
                    #print("volume4.GetMasterVolume(): %s" % volume4.GetMasterVolume())
                    #print(session.Process.name())
        old_poten1 = poten1;  # save the changed value

    if ( poten2 - old_poten2 > tolorence or  old_poten2 - poten2 > tolorence): # check if the current potentiometer value is diffrent than the last saved one while also taking the tolorence into account.
        sessions2 = AudioUtilities.GetAllSessions()
        for session in sessions2:
            volume2 = session._ctl.QueryInterface(ISimpleAudioVolume)
            for app in pot2List:
                if session.Process and session.Process.name() == app: # check if an application with that name is currently running.
                    volume2.SetMasterVolume(abc2, None) # change the volume.
                    #print("volume4.GetMasterVolume(): %s" % volume4.GetMasterVolume())
                    #print(session.Process.name())
        old_poten2 = poten2;  # save the changed value

    if ( poten3 - old_poten3 > tolorence or  old_poten3 - poten3 > tolorence): # check if the current potentiometer value is diffrent than the last saved one while also taking the tolorence into account.
        sessions3 = AudioUtilities.GetAllSessions()
        for session in sessions3:
            volume3 = session._ctl.QueryInterface(ISimpleAudioVolume)
            for app in pot3List:
                if session.Process and session.Process.name() == app: # check if an application with that name is currently running.
                    volume3.SetMasterVolume(abc3, None) # change the volume.
                    #print("volume4.GetMasterVolume(): %s" % volume4.GetMasterVolume())
                    #print(session.Process.name())
        old_poten3 = poten3;  # save the changed value

    if ( poten4 - old_poten4 > tolorence or  old_poten4 - poten4 > tolorence): # check if the current potentiometer value is diffrent than the last saved one while also taking the tolorence into account.
        sessions4 = AudioUtilities.GetAllSessions()
        for session in sessions4:
            volume4 = session._ctl.QueryInterface(ISimpleAudioVolume)
            for app in pot4List:
                if session.Process and session.Process.name() == app: # check if an application with that name is currently running.
                    volume4.SetMasterVolume(abc4, None) # change the volume.
                    #print("volume4.GetMasterVolume(): %s" % volume4.GetMasterVolume())
                    #print(session.Process.name())
        old_poten4 = poten4;  # save the changed value

    #print("\033[H\033[J", end="")

ser.close()
