# automovement.py

import time
import RPi.GPIO as GPIO
import random

BUTTON_PINS = {}
PRESS_TIME = 0.25

def press_button(name):
    """Press any button by name (HIGH = press, LOW = release)."""
    if name not in BUTTON_PINS:
        raise ValueError(f"Unknown button '{name}'")

    pin = BUTTON_PINS[name]
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(PRESS_TIME)
    GPIO.output(pin, GPIO.LOW)

def press_a(): press_button("A")
def press_b(): press_button("B")
def press_x(): press_button("X")
def press_y(): press_button("Y")

def press_up(): press_button("UP")
def press_down(): press_button("DOWN")
def press_left(): press_button("LEFT")
def press_right(): press_button("RIGHT")

def press_start(): press_button("START")
def press_select(): press_button("SELECT")

def press_l(): press_button("L")
def press_r(): press_button("R")

def press_multiple(button_list, hold_time=0.25):
    """Press multiple buttons at the same time."""
    if hold_time is None:
        hold_time = PRESS_TIME

    # Press all buttons (set HIGH)
    for name in button_list:
        pin = BUTTON_PINS[name]
        GPIO.output(pin, GPIO.HIGH)

    time.sleep(hold_time)

    # Release all buttons
    for name in button_list:
        pin = BUTTON_PINS[name]
        GPIO.output(pin, GPIO.LOW)

class SoftReset:
    def reset(self):
        time.sleep(0.5)
        press_multiple(["L", "R", "START", "SELECT"], hold_time=0.25)

    def before_listening_gen4(self):
        """Everything done before waiting for shiny sound."""
        time.sleep(10)  # Wait for game to load
        press_a()
        time.sleep(3)
        press_a()
        time.sleep(3.5)
        press_a()
        time.sleep(3)
        press_a()
        time.sleep(1.5)
        press_a()
        time.sleep(0.5)
        press_a()
        time.sleep(0.5)
        press_a()

    def before_listening_gen5(self):
        time.sleep(11)  # Wait for game to load
        press_a()
        time.sleep(2)
        press_a()
        time.sleep(3.5)
        press_a()
        time.sleep(2)
        press_a()
        time.sleep(4.5)
        press_a()
        time.sleep(1.5)
        press_a()
        time.sleep(0.5)
        press_a()
        time.sleep(0.5)
        press_a()
        time.sleep(0.5)
        press_a()

class RandomEncounter:
    def move(self):
        """Move in a random horizontal direction to avoid walls."""
        direction = random.choice(["LEFT", "RIGHT"])
        if direction == "LEFT":
            press_left()
            time.sleep(0.3)
            press_right()
        else:
            press_right()
            time.sleep(0.3)
            press_left()

    def run(self):
        """Everything done after listening for shiny sound."""
        press_down()
        time.sleep(0.2)
        press_down()
        time.sleep(0.2)
        press_right()
        time.sleep(0.2)
        press_a()
        time.sleep(2) 
        press_a()
        time.sleep(2)



