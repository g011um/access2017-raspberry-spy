#!/usr/bin/python
# Coffee Detector
# Code By: Craig Power, Wesley Takeo-Konrad, Ron Gillies, Greg Hughes
# Modified from:
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Sets an alert condition, sounds a beep when the temperature goes up
# by more than 1 degree celisus.

# Requires:

# Adafruit_DHT, RPi.GPIO

import sys
import Adafruit_DHT #Requires, DHT Interaction
import RPi.GPIO as GPIO  #Requires RPi.GPIO
import time
import smtplib



#HARDWARE VARIABLES
sensor = Adafruit_DHT.AM2302
pin = 4
alert_pin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(alert_pin, GPIO.OUT)
GPIO.output(11, GPIO.LOW)

email_server = "smtp.gmail.com"   # SMTP Server
email_port = 587   # SMTP port
email_login = "pi.temp.access2017@gmail.com"   # Email/Email Login
email_password = "access2017"   # Email Password

on_msg = "THERMAL ALERT - COFFEE DETECTED"   #Message to send when alert = true
off_msg = "THERMAL ALERT CANCELLED - THE THREAT OF COFFEE HAS PASSED"   # message to send when alert returns to false

target_victim = "<insert email address>"

#Variable initialization
sanity_ts = 0
current_state = False
past_state = False


#Read our starting state
initial_humidity, initial_temperature = Adafruit_DHT.read_retry(sensor, pin)
while True:

	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	
	# Un-comment the line below to convert the temperature to Fahrenheit.
	# temperature = temperature * 9/5.0 + 32
	
	# Note that sometimes you won't get a reading and
	# the results will be null (because Linux can't
	# guarantee the timing of calls to read the sensor).
	# If this happens try again!
	
 	print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
	print("warning timestamp: {}".format(sanity_ts))
	if temperature > initial_temperature + 1:
	    current_state = True

	    if(current_state != past_state):
		#this is a state change. Send an email
		past_state = current_state
                server = smtplib.SMTP(email_server, email_port)
		server.starttls()
		server.login(email_login, email_password)
		server.sendmail(email_login, target_victim, on_msg)
		

	    if sanity_ts + 10 <= int(time.time()) :
		    #If it's been ten seconds since the last noise, annoy people
		    time.sleep(0.2)
	            GPIO.output(11, GPIO.HIGH)
		    time.sleep(0.2)
	            GPIO.output(11, GPIO.LOW)
		    time.sleep(0.2)
	            GPIO.output(11, GPIO.HIGH)
		    time.sleep(0.2)
	            GPIO.output(11, GPIO.LOW)
		    sanity_ts = int(time.time())
		    print("warning timestamp: {}".format(sanity_ts))

            GPIO.output(11, GPIO.LOW)
	    print("Coffee Detected - Thermal Warning")
	else:
	    #Alert condition is false
	    current_state = False
	    if(current_state != past_state):
		#this is a state change. Send an email
		past_state = current_state
                server = smtplib.SMTP(email_server, email_port)
		server.starttls()
		server.login(email_login, email_password)
		server.sendmail(email_login, target_victim, off_msg)
	    GPIO.output(11, GPIO.LOW)
	time.sleep(2)
