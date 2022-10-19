#!/usr/bin/env python3

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
  GPIO.output(ledPin,1)

def off():
  print('OFF')
  GPIO.output(ledPin,0)
  
def timenow():
  #now = datetime.now()
  #current_time = now.strftime("%I:%M %p")
  #print(current_time)  
  os.system("kill `ps -ef |grep ffplay |grep -v grep | awk '{print $2}'`")

def roastme():
  print('ROAST ME')
  os.system("kill `ps -ef |grep ffplay |grep -v grep | awk '{print $2}'`")
  song_number = random.randint(1,5)
  song = 'ffplay -autoexit -nodisp /home/pi/songs/song-{name}.mp3 &'.format(name=song_number)
  os.system(song)

def playasong():
  print('PLAY A SONG')
  os.system("kill `ps -ef |grep ffplay |grep -v grep | awk '{print $2}'`")
  song_number = random.randint(1,5)
  song = 'ffplay -autoexit -nodisp /home/pi/songs/song-{name}.mp3 &'.format(name=song_number)
  os.system(song)


if __name__ == '__main__':
    # integers mapped to voice command functions
    commands = {0:nothing, 18:off, 17:on, 19:timenow, 21:roastme, 20:playasong}
    # serial settings
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
      ser.write(serial.to_bytes([0x21])) # import group 1 and await voice input
      time.sleep(0.5)
    print('init complete')
    GPIO.setmode(GPIO.BOARD)      # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPin, GPIO.OUT)   # set ledPin to OUTPUT mode

    try:
      while True:
        data_byte = ser.read() # read serial data (one byte)
        int_val = int.from_bytes(data_byte, byteorder='big') # convert to integer
        print('=========')
        print(int_val)
        commands[int_val]() # call voice command function
    except KeyboardInterrupt:
      print('Exiting Script')
