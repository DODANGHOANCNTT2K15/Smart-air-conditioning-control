# DHT22Controller.py
from GPIOEmulator.EmulatorGUI import GPIO
from DHT22Emulator.DHT22 import readSensor
import config
import time
from updateConfig import update_config_file

def dht22():
    GPIO.setmode(GPIO.BCM)

    while True:
        cur_temp, cur_hum = readSensor(12)
        
        # Chuyển đổi giá trị thành số nguyên (loại bỏ phần thập phân)
        cur_temp = int(cur_temp)
        cur_hum = int(cur_hum)

        # Ghi trực tiếp giá trị vào file config.py
        update_config_file('cur_temp', cur_temp)
        update_config_file('cur_hum', cur_hum)

        time.sleep(0.1)
