# DHT22Controller.py
from GPIOEmulator.EmulatorGUI import GPIO
from DHT22Emulator.DHT22 import readSensor
import config
import time

def dht22():
    GPIO.setmode(GPIO.BCM)

    cur_temp, cur_hum = readSensor(12)
    while True:
        config.cur_hum = cur_hum
        config.cur_temp = cur_temp
        time.sleep(0.1)
