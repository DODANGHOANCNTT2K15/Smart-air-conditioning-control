# LEDController.py
from GPIOEmulator.EmulatorGUI import GPIO
import config
import time

def led_threading():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)

    while True:
        if config.status == True:
            GPIO.output(22, GPIO.LOW) 
        else:
            GPIO.output(22, GPIO.HIGH) 
        time.sleep(0.1)
