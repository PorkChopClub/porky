#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import httplib
import os

import logging
logging.basicConfig(
        filename='/var/log/porky.log',
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
        )
logging.debug('PorkyPi started')

def porkput(path):
    logging.info("Request:  PUT " + path)
    api_key = os.getenv("API_KEY")
    conn = httplib.HTTPConnection("porkchop.freerunningtech.com")
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn.request('PUT', path, "table_token="+api_key, headers)
    result = conn.getresponse()
    logging.info("Response: " + str(result.status) + " " + str(result.reason))
    conn.close()

def homeButton(channel):
    porkput("/api/table/home_button")

def awayButton(channel):
    porkput("/api/table/away_button")

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
#GPIO.add_event_detect(23, GPIO.RISING, callback=homeButton, bouncetime=1000)
#GPIO.add_event_detect(24, GPIO.RISING, callback=awayButton, bouncetime=1000)

def waitForDown(pin):
	while GPIO.input(pin):
		time.sleep(0.05)

while True:
	if GPIO.input(23):
		homeButton(23)
		waitForDown(23)
		time.sleep(0.5)
	if GPIO.input(24):
		awayButton(24)
		waitForDown(24)
		time.sleep(0.5)
	time.sleep(0.05)

GPIO.cleanup()
