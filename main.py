from time import sleep

__author__ = 'Jesse'

from machine import I2C, Pin
from esp8266_i2c_lcd import I2cLcd


class main:
    @staticmethod
    def run():
        sleep(5)  # Wait for network
        i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
        lcd = I2cLcd(i2c, 0x27, 4, 20)
        lcd.putstr('Hello World!')

if __name__ == "__main__":
    main.run()
