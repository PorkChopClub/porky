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
    conn = httplib.HTTPConnection("porkchop.club")
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn.request('PUT', path, "table_token="+api_key, headers)
    result = conn.getresponse()
    logging.info("Response: " + str(result.status) + " " + str(result.reason))
    conn.close()

def homeButton(channel):
    porkput("/api/table/home_button")

def awayButton(channel):
    porkput("/api/table/away_button")

HOME_BUTT = 23
AWAY_BUTT = 24
HOME_LED = 25
AWAY_LED = 17


GPIO.setmode(GPIO.BCM)
GPIO.setup(HOME_BUTT, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(AWAY_BUTT, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.setup(HOME_LED, GPIO.OUT, initial = 0)
GPIO.setup(AWAY_LED, GPIO.OUT, initial = 0)


def waitForDown(pin):
	while GPIO.input(pin):
		time.sleep(0.05)

while True:
	if GPIO.input(HOME_BUTT):
		GPIO.output(HOME_LED, GPIO.HIGH)
		homeButton(HOME_BUTT)
		waitForDown(HOME_BUTT)
		time.sleep(0.5)
		GPIO.output(HOME_LED, GPIO.LOW)
	if GPIO.input(AWAY_BUTT):
		GPIO.output(AWAY_LED, GPIO.HIGH)
		awayButton(AWAY_BUTT)
		waitForDown(AWAY_BUTT)
		time.sleep(0.5)
		GPIO.output(AWAY_LED, GPIO.LOW)
	time.sleep(0.05)

GPIO.cleanup()
