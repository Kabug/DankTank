from pynput import keyboard
from gpiozero import Robot
import RPi.GPIO as GPIO
import time
import os

run = True
robot = Robot(left=(8,25), right=(1,7))
fixedUpdate = 0.02
controls = {
    "w": "forward",
    "s": "backward",
    "a": "left",
    "d": "right"
}

def on_press(key):
    try:
        print("pressed {0}".format(key.char))
        if key.char in controls:
            if key.char == ("w"):
                robot.forward()
            elif key.char == ("s"):
                robot.backward()
            elif key.char == ("d"):
                robot.right()
            elif key.char == ("a"):
                robot.left()
        else:
            robot.stop()
    except AttributeError:
        print("special press {0}".format(key))

def on_release(key):
    global run
    try:
        print("{0} released".format(key))
        if key == keyboard.Key.esc:
            run = False
            return False
        else:
            robot.stop()
    except AttributeError:
        print("special press {0}".format(key))

kblistener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
kblistener.start() 
    
while run == True:
    time.sleep(fixedUpdate)

kblistener.stop()