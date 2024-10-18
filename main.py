from GPIOEmulator.EmulatorGUI import GPIO
from LCDpnh.pnhLCD1602 import LCD1602
from DHT22Emulator.DHT22 import readSensor
import config
import time
import threading
import time
import connect
from voiceController import voice_control 
from LEDController import led_threading
from DHT22Controller import dht22
from LCDController import lcd


def main():
    lcd_thread = threading.Thread(target=lcd)
    button_thread = threading.Thread(target=button)
    dht22_thread = threading.Thread(target=dht22)
    led_thread = threading.Thread(target=led_threading)
    connect_thread = threading.Thread(target=connect.run_flask)

    lcd_thread.start()
    button_thread.start()
    dht22_thread.start()
    led_thread.start()
    connect_thread.start()

    lcd_thread.join()
    button_thread.join()
    dht22_thread.join()
    led_thread.join()

def status_after_delay(delay):
    time.sleep(delay)
    config.status = False
    config.time_on = 0
    print("Đã tắt")

def button():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while True:
        if GPIO.input(18) == GPIO.LOW:  
            config.status = not config.status
            time.sleep(0.5) 
        if GPIO.input(19) == GPIO.LOW and config.temperature < 31: 
            config.temperature += 1
            time.sleep(0.5)
        if GPIO.input(20) == GPIO.LOW and config.temperature > 16:
            config.temperature -= 1
            time.sleep(0.5)
        if GPIO.input(21) == GPIO.LOW:
            config.current_mode_index = (config.current_mode_index + 1) % 5
            time.sleep(0.5)
        if GPIO.input(16) == GPIO.LOW:
            config.page = (config.page + 1) % 4
            time.sleep(0.5)
        if GPIO.input(15) == GPIO.LOW:
            config.current_wind_index = (config.current_wind_index + 1) % 3
            time.sleep(0.5)
        if GPIO.input(14) == GPIO.LOW :
            config.time_on = (config.time_on + 1) % 13
            if config.time_on == 0:
                config.time_set = False
            else:
                config.time_set = True
                status_thread = threading.Thread(target=status_after_delay, args=(10 * config.time_on,))
                status_thread.start()
            time.sleep(0.5)
        if GPIO.input(13) == GPIO.LOW:
            voice_control()
            time.sleep(0.5)

if __name__ == '__main__':
    main()