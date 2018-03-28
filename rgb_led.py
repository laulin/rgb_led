#! /usr/bin/env python3

# This script manages a rgb led on RPI GPIO. By default, red i on pin 26, green on pin 19 and blue on pin
# 13. The pattern format is like (\d*[rgbwv])+. For example 3rw2bg will create an pattern like
# "rrrwbbvg"; The time base is 50 ms, so you will get 150 ms of red, 50 ms of white, 100 ms of blue,
# 50 ms of black and 50 ms of green. It will loop forever.


import re
from itertools import cycle
import time
import argparse

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# pins definition (default)
RED_PIN = 26
GREEN_PIN = 19
BLUE_PIN = 13

def parse_args():
    # parse argument from CLI
    # run with -h for help
    parser = argparse.ArgumentParser(description='Manages one RGB led using GPIO. Designed by laulin')
    parser.add_argument('-r', '--red-pin', type=int, default=RED_PIN, help='The pin number of the red color (BCM). Default is {}'.format(RED_PIN))
    parser.add_argument('-g', '--green-pin', type=int, default=GREEN_PIN, help='The pin number of the green color (BCM). Default is {}'.format(GREEN_PIN))
    parser.add_argument('-b', '--blue-pin', type=int, default=BLUE_PIN, help='The pin number of the blue color (BCM). Default is {}'.format(BLUE_PIN))
    parser.add_argument('pattern', nargs='+', help="Define the color pattern. format : (\d*[rgbwv])+")
    return parser.parse_args()


def init(red_pin, green_pin, blue_pin):
    GPIO.setup(blue_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(green_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(red_pin, GPIO.OUT, initial=GPIO.LOW)

def parse_pattern(pattern):
    # this function takes a pattern in format number (optional) + a letter (mandatory). 
    # Letter must be r,g,b,w or v for red, green, blue, white, void (black, but b was used).

    # example 3rb2wgg -> rrrbwwgg
    states = re.findall(r'(\d*)([rgbwv])', pattern.lower())
    expanded = [value if not number else value*int(number) for number, value in states]
    return "".join(expanded)

def set_color(color):
    # takes a color letter and display it on led

    # reset
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)

    if color == "r":
        GPIO.output(RED_PIN, GPIO.HIGH)
    elif color == "g":
        GPIO.output(GREEN_PIN, GPIO.HIGH)
    elif color == "b":
        GPIO.output(BLUE_PIN, GPIO.HIGH)
    elif color == "w":
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.HIGH)
    else:
        pass

def process(patterns, red_pin, green_pin, blue_pin):
    # It inits output and browse color each 50 ms forever
    
    init(red_pin, green_pin, blue_pin)

    pattern = "".join(patterns)
    color_states = parse_pattern(pattern)

    for color in cycle(color_states):
        set_color(color)
        time.sleep(0.05)


if __name__ == "__main__":
    args = parse_args()

    try:
        process(args.pattern, args.red_pin, args.green_pin, args.blue_pin)
    except KeyboardInterrupt:
        GPIO.cleanup()


