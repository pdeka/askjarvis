#!/usr/bin/env python3
 #now = datetime.now()
 #current_time = now.strftime("%I:%M %p")
 #print(current_time)  

from datetime import datetime

import RPi.GPIO as GPIO
import time
import serial
import os
import random


ledPin = 12    # define ledPin

# voice command functions
def empty():
  pass

def nothing():
  print('--')

def on():
  print('ON')  
  song = 'ffplay -autoexit -nodisp /home/pi/songs/lightson.mp3 &'
  os.system(song)
  GPIO.output(ledPin,1)

def off():
  print('OFF')
  song = 'ffplay -autoexit -nodisp /home/pi/songs/shutdown.mp3 &'
  os.system(song)
  GPIO.output(ledPin,0)
  
def stopplaying():
  os.system("kill `ps -ef |grep ffplay |grep -v grep | awk '{print $2}'`")

def playasong():
  print('PLAY A SONG')
  os.system("kill `ps -ef |grep ffplay |grep -v grep | awk '{print $2}'`")
  song_number = random.randint(1,5)
  song = 'ffplay -autoexit -nodisp /home/pi/songs/song-{name}.mp3 &'.format(name=song_number)
  os.system(song)

def timenow():
  print('TIME NOW')
  os.system("kill `ps -ef |grep ffplay |grep -v grep | awk '{print $2}'`")
  os.system('espeak 2:45PM')


def initialize():
  global ser
  # serial settings
  try: ser
  except NameError: print('Serial port not defined')
  else: ser.close()

  ser = serial.Serial(
      port='/dev/ttyUSB0',
      baudrate=9600,
      parity=serial.PARITY_NONE,
      stopbits=serial.STOPBITS_ONE,
      bytesize=serial.EIGHTBITS,
      timeout=1
  )
  ser.flushInput()

  # run twice to make sure it's in the correct mode
  for i in range(2):
    ser.write(serial.to_bytes([0x00])) # set speech module to waiting state
    time.sleep(0.5)
    ser.write(serial.to_bytes([0xAA])) # set speech module to waiting state
    time.sleep(0.5)
    ser.write(serial.to_bytes([0x21]))       
    time.sleep(0.5)
  print('init complete')



if __name__ == '__main__':
   global ser

   commands = {0:nothing, 18:off, 17:on, 19:stopplaying, 21:timenow, 20:playasong}

   initialize()
   GPIO.setmode(GPIO.BOARD)      # use PHYSICAL GPIO Numbering
   GPIO.setup(ledPin, GPIO.OUT)   # set ledPin to OUTPUT mode

   try:
     while True:
       data_byte = ser.read() # read serial data (one byte)
       int_val = int.from_bytes(data_byte, byteorder='big') # convert to integer      
       print(int_val)
       commands[int_val]() # call voice command function
   except KeyboardInterrupt:
     print('Exiting Script')
