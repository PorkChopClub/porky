#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import httplib
import os

def porkput(path):
    print("PUT " + path)
    api_key = os.getenv("API_KEY")
    conn = httplib.HTTPSConnection("porkchop.freerunningtech.com")
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn.request('PUT', path, "table_token="+api_key, headers)
    result = conn.getresponse()
    print(result.status)
    conn.close()

def homeButton(channel):
    porkput("/api/table/home_button")

def awayButton(channel):
    porkput("/api/table/away_button")

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(23, GPIO.RISING, callback=homeButton, bouncetime=1000)
GPIO.add_event_detect(24, GPIO.RISING, callback=awayButton, bouncetime=1000)

while True:
        print("1")
        time.sleep(1)

GPIO.cleanup()
