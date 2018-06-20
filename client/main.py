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



lcd_obj = lcd_helper()


class main:
    @staticmethod
    def do_connect():
        lcd_obj.write_lcd('Setting Up Network...')
        sta_if = network.WLAN(network.STA_IF)
        if sta_if.isconnected():
            sleep(2)
            lcd_obj.write_lcd(str(sta_if.ifconfig()))
            sleep(2)
        else:
            lcd_obj.write_lcd('Retrying connection')
            sta_if.active(True)
            sleep(2)
            lcd_obj.write_lcd(str(sta_if.ifconfig()))
            sleep(2)
            if not sta_if.isconnected():
                lcd_obj.write_lcd('Cannot connect, rebooting...')
                reset()


    @staticmethod
    def sub_cb(topic, msg):
        # print(topic,msg)
        topic_s = topic.decode("utf-8")
        msg_s = msg.decode("utf-8")
        # print(topic_s,msg_s)

        if topic_s == 'lcd/message':
            lcd_obj.write_lcd(msg_s)
        if topic_s == 'lcd/backlight':
            if msg_s == '1':
                lcd_obj.lcd.backlight_on()
            else:
                lcd_obj.lcd.backlight_off()
        if topic_s == 'lcd/move':
            try:
                x = int(str(msg_s).split(',')[0])
                y = int(str(msg_s).split(',')[1])
                lcd_obj.lcd.move_to(x,y)
            except:
                lcd_obj.write_lcd('invalid cursor location')
        if topic_s == 'lcd/write':
            lcd_obj.lcd.putstr(msg_s)
        if topic_s == 'lcd/clear':
            lcd_obj.lcd.clear()

    @staticmethod
    def run():
        c = simple.MQTTClient(server=mqtt_creds.server, client_id='lcd-micropython', user=mqtt_creds.username,
                              password=mqtt_creds.password)
        c.set_callback(main.sub_cb)

        try:
            c.connect()
            c.subscribe(b"lcd/#")
            while True:
                c.wait_msg()
        except:
            lcd_obj.write_lcd('Cannot connect to server')
            sleep(4)
            reset()  # When in doubt, REBOOT


if __name__ == "__main__":
    main.do_connect()
    sleep(5)  # Wait for network
    lcd_obj.write_lcd('READY NOW')
    main.run()
