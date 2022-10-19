import RPi.GPIO as GPIO
import time

ledPin = 12    # define ledPin

def setup():   
    GPIO.setmode(GPIO.BOARD)      # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPin, GPIO.OUT)   # set ledPin to OUTPUT mode

def loop():
    while True:
        GPIO.output(ledPin,1)   # turn on led
        print ('led turned on >>>')     # print information on terminal
        time.sleep(2)
        GPIO.output(ledPin,0) # turn off led 
        print ('led turned off <<<')    
        time.sleep(2)

def destroy():
    GPIO.output(ledPin, GPIO.LOW)     # turn off led 
    GPIO.cleanup()                    # Release GPIO resource

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()