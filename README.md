# Screencap
## A simple ffmpeg wrapper for easy screen recording


Requires:

- python-xlib


Usage: ./screencap.py fileName (omit extension)

ctrl + f9 starts and stops recording.
File gets recorded as an mkv which can then be re-encoded to be smaller by the user if needed.

There is no conf file, the script is simple to edit. To change the ffmpeg command (for example to change the recording resolution, default is 1920x1080 at 25fps), edit the captureCmd variable in the script.