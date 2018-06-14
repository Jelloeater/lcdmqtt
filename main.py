from time import sleep

__author__ = 'Jesse'
import json, esp, machine
from machine import I2C, Pin
import urequests as requests
from esp8266_i2c_lcd import I2cLcd

DEFAULT_I2C_ADDR = 0x27

class main:
    @staticmethod
    def run():
        sleep(5)  # Wait for network

        i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
        lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 4, 20)
        lcd.backlight_off()
        lcd.display_on()
        lcd.blink_cursor_off()
        lcd.hide_cursor()
        lcd.clear()
        lcd.backlight_on()
        lcd.putstr("It Works!\nSecond Line")

if __name__ == "__main__":
    main.run()
