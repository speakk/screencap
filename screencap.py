#!/usr/bin/env python3

import os 
try:
    import pyxhook 
except ModuleNotFoundError as err:
    print("This script has a dependency which requires python-xlib to be installed. Be sure to install python-xlib")
    print(err)
    exit()

import subprocess
import sys

if len(sys.argv) < 2:
    print("No filename supplied.")
    print("Usage: python screenCap.py [filename].  (omit the extension, .mkv will be added by the script)")
    sys.exit()

fileName = sys.argv[1] + ".mkv"

if os.path.isfile(fileName):
    print("File already exists: " + fileName + ".(mp4|mkv)")
    overwrite = input("Do you want to overwrite the file(s)? y/n \n")
    if overwrite == 'n':
        sys.exit()
    elif overwrite != 'y':
        print("Neither yes or no, exiting until you make up your mind")
        sys.exit()

print("Ready to capture on: ctrl + f9")

captureCmd = "ffmpeg -y -f x11grab -r 25 -s 1920x1080 -i :0.0 -vcodec libx264 -preset ultrafast -threads 0 " + fileName

isLCtrlDown = False
isRCtrlDown = False

capturing = False
captureProcess = None

new_hook = pyxhook.HookManager() 
  
def OnKeyPress(event): 
    global isLCtrlDown
    global isRCtrlDown
    global captureProcess

    if event.Key == "Control_L":
        isLCtrlDown = True

    if event.Key == "Control_R":
        isRCtrlDown = True

    if event.Key == 'q':
        global new_hook
        if captureProcess:
            captureProcess.terminate()
            captureProcess.wait()
            new_hook.cancel()
        print("Exiting...")
        exit()

    if event.Key == "F9" and (isLCtrlDown or isRCtrlDown):
        if not captureProcess:
            print("Starting capture!")
            captureProcess = subprocess.Popen(captureCmd, shell=True)
        else:
            captureProcess.terminate()
            captureProcess.wait()
            if not os.path.isfile(fileName):
                print ("General capture FAIL. Exiting...")
                exit()
            print("Recording finished, file written: " + fileName)
            print("Ready to capture again with ctrl + f9. Exit with q or ctrl+c.")
            captureProcess = None

def OnKeyUp(event):
    global isLCtrlDown
    global isRCtrlDown
    if event.Key == "Control_L":
        isLCtrlDown = False

    if event.Key == "Control_R":
        isRCtrlDown = False

new_hook.KeyDown = OnKeyPress 
new_hook.KeyUp = OnKeyUp 
new_hook.HookKeyboard() 
  
new_hook.start()
