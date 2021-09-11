from pynput import keyboard
from gpiozero import Robot
import RPi.GPIO as GPIO
import time
import os

run = True
direction_state = [False, False, False, False] # W,A,S,D
# robot = Robot(left=(23,22), right=(27,17))
GPIO.setmode(GPIO.BCM)
left_motor = [22, 23]
right_motor = [17, 27]
GPIO.setup(23, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
speed = 1
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
                direction_state[0] = True
            elif key.char == ("a"):
                direction_state[1] = True
            elif key.char == ("s"):
                direction_state[2] = True
            elif key.char == ("d"):
                direction_state[3] = True
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
            direction_state[0] = False
        elif key.char == ("a"):
            direction_state[1] = False
        elif key.char == ("s"):
            direction_state[2] = False
        elif key.char == ("d"):
            direction_state[3] = False
        else:
            robot.stop()
    except AttributeError:
        print("special press {0}".format(key))


kblistener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
kblistener.start() 
    
while run == True:
    if direction_state[0]:
        GPIO.output(left_motor[0], GPIO.HIGH)
        GPIO.output(left_motor[1], GPIO.LOW)
        GPIO.output(right_motor[0], GPIO.HIGH)
        GPIO.output(right_motor[1], GPIO.LOW)
        time.sleep(0.0003)
        GPIO.output(left_motor[0], GPIO.LOW)
        time.sleep(0.0003)
        GPIO.output(left_motor[0], GPIO.HIGH)
    elif direction_state[1]:
        pass
        GPIO.output(left_motor[0], GPIO.LOW)
        GPIO.output(left_motor[1], GPIO.HIGH)
        GPIO.output(right_motor[0], GPIO.HIGH)
        GPIO.output(right_motor[1], GPIO.LOW)
    elif direction_state[2]:
        GPIO.output(left_motor[0], GPIO.LOW)
        GPIO.output(left_motor[1], GPIO.HIGH)
        GPIO.output(right_motor[0], GPIO.LOW)
        GPIO.output(right_motor[1], GPIO.HIGH)
        time.sleep(0.0003)
        GPIO.output(left_motor[0], GPIO.HIGH)
        time.sleep(0.0003)
        GPIO.output(left_motor[0], GPIO.LOW)
        pass
    elif direction_state[3]:
        GPIO.output(left_motor[0], GPIO.HIGH)
        GPIO.output(left_motor[1], GPIO.LOW)
        GPIO.output(right_motor[0], GPIO.LOW)
        GPIO.output(right_motor[1], GPIO.HIGH)
        pass
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

