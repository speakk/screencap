#!/usr/bin/env python3

import os 
import pyxhook 
import subprocess
import sys

if len(sys.argv) < 2:
    print("No filename supplied. Usage: python screenCap.py [filename].  (omit the extension, .mkv will be added by the script)")
    exit()

fileName = sys.argv[1]
  
# Allow setting the cancel key from environment args, Default: ` 
cancel_key = ord( 
    os.environ.get( 
        'pylogger_cancel', 
        '`'
    )[0] 
) 

fileName = fileName + ".mkv"
if os.path.isfile(fileName):
    print("File already exists: " + fileName + ".(mp4|mkv)")
    overwrite = input("Do you want to overwrite the file(s)? y/n \n")
    if overwrite == 'n':
        exit()
    elif overwrite != 'y':
        print("Neither yes or no, exiting until you make up your mind")
        exit()

print("Ready to capture on: ctrl + f9")

captureCmd = "ffmpeg -y -f x11grab -r 25 -s 1920x1080 -i :0.0 -vcodec libx264 -preset ultrafast -threads 0 " + fileName

isLCtrlDown = False
isRCtrlDown = False

capturing = False
captureProcess = None
convertProcess = None

# create a hook manager object 
new_hook = pyxhook.HookManager() 
  
#creating key pressing event and saving it into log file 
def OnKeyPress(event): 
    global isLCtrlDown
    global isRCtrlDown
    global captureCmd
    global capturing
    global captureProcess

    if event.Key == "Control_L":
        isLCtrlDown = True

    if event.Key == "Control_R":
        isRCtrlDown = True

    if event.Key == 'q':
        global new_hook
        if capturing:
            captureProcess.terminate()
            captureProcess.wait()
            new_hook.cancel()
        print("Exiting...")
        exit()

    if event.Key == "F9" and (isLCtrlDown or isRCtrlDown):
        if not capturing:
            print("Starting capture!")
            captureProcess = subprocess.Popen(captureCmd, shell=True)
            capturing = True
        else:
            captureProcess.terminate()
            captureProcess.wait()
            if not os.path.isfile(fileName):
                print ("General capture FAIL. Exiting...")
                exit()
            print("Recording finished, file written: " + fileName)
            print("Ready to capture again with ctrl + f9. Exit with q or ctrl+c.")
            capturing = False

def OnKeyUp(event):
    global isLCtrlDown
    global isRCtrlDown
    if event.Key == "Control_L":
        isLCtrlDown = False

    if event.Key == "Control_R":
        isRCtrlDown = False

new_hook.KeyDown = OnKeyPress 
new_hook.KeyUp = OnKeyUp 
# set the hook 
new_hook.HookKeyboard() 
  
try: 
    new_hook.start()         # start the hook 
except KeyboardInterrupt: 
    # User cancelled from command line. 
    pass
except Exception as ex: 
    # Write exceptions to the log file, for analysis later. 
    msg = 'Error while catching events:\n  {}'.format(ex) 
    pyxhook.print_err(msg) 
    # with open(log_file, 'a') as f: 
    #     f.write('\n{}'.format(msg)) 
