from time import sleep

__author__ = 'Jesse'

from machine import Pin, I2C, reset
from esp8266_i2c_lcd import I2cLcd
import simple
import mqtt_creds
import network

DEFAULT_I2C_ADDR = 0x27


class lcd_helper:
    def __init__(self):
        self.i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
        self.lcd = I2cLcd(self.i2c, DEFAULT_I2C_ADDR, 4, 20)

    def write_lcd(self, msg):
        self.lcd.clear()
        self.lcd.putstr(msg)


lcd = lcd_helper()


class main:
    @staticmethod
    def do_connect():
        lcd.write_lcd('Setting Up Network...')
        sta_if = network.WLAN(network.STA_IF)
        if sta_if.isconnected():
            sleep(2)
            lcd.write_lcd(str(sta_if.ifconfig()))
            sleep(2)
        else:
            lcd.write_lcd('Retrying connection')
            sta_if.active(True)
            sleep(2)
            lcd.write_lcd(str(sta_if.ifconfig()))
            sleep(2)
            if not sta_if.isconnected():
                lcd.write_lcd('Cannot connect, rebooting...')
                reset()


    @staticmethod
    def sub_cb(topic, msg):
        print((topic, msg))
        lcd.write_lcd(msg.decode("utf-8"))

    @staticmethod
    def run():
        c = simple.MQTTClient(server=mqtt_creds.server, client_id='lcd-micropython', user=mqtt_creds.username,
                              password=mqtt_creds.password)
        c.set_callback(main.sub_cb)

        try:
            c.connect()
            c.subscribe(b"lcd_msg")
            while True:
                c.wait_msg()
        except:
            lcd.write_lcd('Cannot connect to server')
            sleep(4)
            reset()  # When in doubt, REBOOT


if __name__ == "__main__":
    main.do_connect()
    sleep(5)  # Wait for network
    lcd.write_lcd('READY NOW')
    main.run()
