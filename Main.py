from picamera import PiCamera
from pynput import keyboard
import RPi.GPIO as GPIO
import time
import os

# Initial Values
 
GPIO.setmode(GPIO.BCM)
left_motor = [22, 23]
right_motor = [17, 27]
GPIO.setup(23, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

camera = PiCamera()
camera.rotation = 180

speed = 1
correction = 0.0003
run = True
controls_state = {
    "w": False, # Forward
    "a": False, # Left
    "s": False, # Backward
    "d": False, # Right
    "c": False  # Camera
}

# Keyboard Listener

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
            elif key.char == ("c"):
                controls_state["c"] = not(controls_state["c"])
        else:
            stop()
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
            stop()
    except AttributeError:
        print("special press {0}".format(key))


kblistener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
kblistener.start() 

# Movement Functions

def go_forwards():
    GPIO.output(left_motor[0], GPIO.HIGH)
    GPIO.output(left_motor[1], GPIO.LOW)
    GPIO.output(right_motor[0], GPIO.HIGH)
    GPIO.output(right_motor[1], GPIO.LOW)
    time.sleep(correction)
    GPIO.output(left_motor[0], GPIO.LOW)
    time.sleep(correction)
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
    time.sleep(correction)
    GPIO.output(left_motor[0], GPIO.HIGH)
    time.sleep(correction)
    GPIO.output(left_motor[0], GPIO.LOW)

def go_right():
    GPIO.output(left_motor[0], GPIO.HIGH)
    GPIO.output(left_motor[1], GPIO.LOW)
    GPIO.output(right_motor[0], GPIO.LOW)
    GPIO.output(right_motor[1], GPIO.HIGH)

def go_forward_right():
    GPIO.output(left_motor[0], GPIO.HIGH)
    GPIO.output(left_motor[1], GPIO.LOW)
    GPIO.output(right_motor[0], GPIO.HIGH)
    GPIO.output(right_motor[1], GPIO.LOW)
    time.sleep(correction * 5)
    GPIO.output(right_motor[0], GPIO.LOW)
    time.sleep(correction * 5)
    GPIO.output(right_motor[0], GPIO.HIGH)

def go_forward_left():
    GPIO.output(left_motor[0], GPIO.HIGH)
    GPIO.output(left_motor[1], GPIO.LOW)
    GPIO.output(right_motor[0], GPIO.HIGH)
    GPIO.output(right_motor[1], GPIO.LOW)
    time.sleep(correction * 500)
    GPIO.output(left_motor[0], GPIO.LOW)
    time.sleep(correction * 500)
    GPIO.output(left_motor[0], GPIO.HIGH)

def stop():
    GPIO.output(left_motor[0], GPIO.LOW)
    GPIO.output(left_motor[1], GPIO.LOW)
    GPIO.output(right_motor[0], GPIO.LOW)
    GPIO.output(right_motor[1], GPIO.LOW)

# Main Loop

while run == True:
    if controls_state["w"]:
        if controls_state["d"]:
            go_forward_right()
        elif controls_state["a"]:
            go_forward_left()
        elif controls_state["s"]:
            stop()
        else:
            go_forwards()
    elif controls_state["a"]:
        go_left()
    elif controls_state["s"]:
        go_backwards()
    elif controls_state["d"]:
        go_right()
    
    if controls_state["c"]:
        camera.start_preview()
    
    onTime = 0.001
    if speed == 0:
        onTime = 0
        offTime = 0.001
    else:
        offTime = onTime / speed - onTime
    time.sleep(onTime)
    stop()
    time.sleep(offTime)

# Cleanup

kblistener.stop()
camera.close()
GPIO.cleanup()
