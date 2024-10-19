# LCDController.py
from GPIOEmulator.EmulatorGUI import GPIO
from LCDpnh.pnhLCD1602 import LCD1602
import config
import time

def lcd():
    try:
        lcd = LCD1602()

        lcd.clear()

        GPIO.setmode(GPIO.BCM)

        last_gpio_activity = time.time()
        
        while True:
            stateAC = config.stateAC

            if (GPIO.input(15) == GPIO.LOW or 
                GPIO.input(16) == GPIO.LOW or 
                GPIO.input(19) == GPIO.LOW or 
                GPIO.input(20) == GPIO.LOW or 
                GPIO.input(21) == GPIO.LOW or
                GPIO.input(18) == GPIO.LOW):
                
                last_gpio_activity = time.time()
                config.stateAC = not stateAC

            if stateAC:
                lcd.clear()
                lcd.backlight_on()
                display(lcd)
                continue

            if not config.status:
                lcd.clear()
                lcd.backlight_off()
                config.stateAC = False
                display(lcd)

            if stateAC and (time.time() - last_gpio_activity > 5):
                lcd.clear()
                lcd.backlight_off()
                config.stateAC = False
                display(lcd)
            
    except Exception as e:
        print(f"LCD Error: {e}")
    finally:
        lcd.close()

def display(lcd):
    match config.page:
        case 0:
            page_1(lcd)
        case 1:
            current_mode = config.current_mode_index
            current_speed = config.current_wind_index
            page_2(lcd, current_mode, current_speed)
        case 2:
            page_3(lcd)
        case 3:
            page_4(lcd)


def page_1(lcd):
    lcd.write_string(str(f"Temp: {config.temperature:.0f}°C"))
    lcd.set_cursor(1, 0)
    lcd.write_string(str(f"Hum: {config.cur_hum:.0f}%"))
    time.sleep(0.1)


def page_2(lcd, mode, speed):
    lcd.write_string(str(f"Fan Speed: {config.wind_speed[speed]}"))
    lcd.set_cursor(1, 0)
    lcd.write_string(str(f"Mode: {config.modes[mode]}"))
    time.sleep(0.1)


def page_3(lcd):
    lcd.write_string(str(f"Time on: {config.time_on}"))
    lcd.set_cursor(1, 0)
    lcd.write_string(str(f"Time set: {config.time_set}"))
    time.sleep(0.1)


def page_4(lcd):
    lcd.write_string(str(f"Now Temp: {config.cur_temp:.0f}"))
    lcd.set_cursor(1, 0)
    lcd.write_string(str(f"Now Hum: {config.cur_hum:.0f}"))
    time.sleep(0.1)
