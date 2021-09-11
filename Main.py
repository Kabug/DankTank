from pynput import keyboard
from gpiozero import Robot
import RPi.GPIO as GPIO
import time
import os

run = True
GPIO.setmode(GPIO.BCM)
left_motor = [22, 23]
right_motor = [17, 27]
GPIO.setup(23, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
speed = 1
controls_state = {
    "w": False,
    "s": False,
    "a": False,
    "d": False
}

def on_press(key):
    try:
        print("pressed {0}".format(key.char))
        if key.char in controls_state:
            if key.char == ("w"):
                controls_state["w"] = True
            elif key.char == ("a"):
                controls_state["a"] = True
            elif key.char == ("s"):
                controls_state["s"] = True
            elif key.char == ("d"):
                controls_state["d"] = True
        else:
            #robot.stop()
            pass
    except AttributeError:
        print("special press {0}".format(key))

def on_release(key):
    global run
    try:
        print("{0} released".format(key))
        if key == keyboard.Key.esc:
            run = False
        elif key.char == ("w"):
            controls_state["w"] = False
        elif key.char == ("a"):
            controls_state["a"] = False
        elif key.char == ("s"):
            controls_state["s"] = False
        elif key.char == ("d"):
            controls_state["d"] = False
        else:
            GPIO.output(left_motor[0], GPIO.LOW)
            GPIO.output(left_motor[1], GPIO.LOW)
            GPIO.output(right_motor[0], GPIO.LOW)
            GPIO.output(right_motor[1], GPIO.LOW)
    except AttributeError:
        print("special press {0}".format(key))


kblistener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
kblistener.start() 

def go_forwards():
    GPIO.output(left_motor[0], GPIO.HIGH)
    GPIO.output(left_motor[1], GPIO.LOW)
    GPIO.output(right_motor[0], GPIO.HIGH)
    GPIO.output(right_motor[1], GPIO.LOW)
    time.sleep(0.0003)
    GPIO.output(left_motor[0], GPIO.LOW)
    time.sleep(0.0003)
    GPIO.output(left_motor[0], GPIO.HIGH)

def go_left():
     GPIO.output(left_motor[0], GPIO.LOW)
     GPIO.output(left_motor[1], GPIO.HIGH)
     GPIO.output(right_motor[0], GPIO.HIGH)
     GPIO.output(right_motor[1], GPIO.LOW)

def go_backwards():     
    GPIO.output(left_motor[0], GPIO.LOW)
    GPIO.output(left_motor[1], GPIO.HIGH)
    GPIO.output(right_motor[0], GPIO.LOW)
    GPIO.output(right_motor[1], GPIO.HIGH)
    time.sleep(0.0003)
    GPIO.output(left_motor[0], GPIO.HIGH)
    time.sleep(0.0003)
    GPIO.output(left_motor[0], GPIO.LOW)

def go_right():
    GPIO.output(left_motor[0], GPIO.HIGH)
    GPIO.output(left_motor[1], GPIO.LOW)
    GPIO.output(right_motor[0], GPIO.LOW)
    GPIO.output(right_motor[1], GPIO.HIGH)

while run == True:
    if controls_state["w"]:
        go_forwards()
    elif controls_state["a"]:
        go_left()
    elif controls_state["s"]:
        go_backwards()
    elif controls_state["d"]:
        go_right()

    onTime = 0.001
    if speed == 0:
        onTime = 0
        offTime = 0.001
    else:
        offTime = onTime / speed - onTime
    time.sleep(onTime)
    GPIO.output(left_motor[0], GPIO.LOW)
    GPIO.output(left_motor[1], GPIO.LOW)
    GPIO.output(right_motor[0], GPIO.LOW)
    GPIO.output(right_motor[1], GPIO.LOW)
    time.sleep(offTime)

kblistener.stop()
GPIO.cleanup()
