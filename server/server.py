__author__ = 'Jesse'
import logging

logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)",
                    level=logging.INFO,
                    # filename='autobot.log'  #Logging to file disabled
                    )

import paho.mqtt.client as mqtt
import mqtt_creds_server  # Rename mqtt_creds_example and fill in your own info
import datetime
import pytz
from time import sleep
from weather import Weather, Unit

client = mqtt.Client()
client.username_pw_set(mqtt_creds_server.username, mqtt_creds_server.password)
client.connect(mqtt_creds_server.server, 1883, 60)


def write_weather():
    w = Weather(unit=Unit.FAHRENHEIT)
    l = w.lookup(mqtt_creds_server.yahoo_world_id)

    # Write Temp
    client.publish('lcd/move', '0,1', qos=0, retain=False)
    client.publish('lcd/write', 'Temp:', qos=0, retain=False)
    client.publish('lcd/move', '5,1', qos=0, retain=False)
    client.publish('lcd/write', '     ', qos=0, retain=False)  # Clear line for 20 char wide LCD
    client.publish('lcd/move', '5,1', qos=0, retain=False)
    client.publish('lcd/write', str(l.condition.temp + 'F'), qos=0, retain=False)

    # Write Humidity
    client.publish('lcd/move', '10,1', qos=0, retain=False)
    client.publish('lcd/write', 'Humid:', qos=0, retain=False)
    client.publish('lcd/move', '16,1', qos=0, retain=False)
    client.publish('lcd/write', '    ', qos=0, retain=False)  # Clear line for 20 char wide LCD
    client.publish('lcd/move', '16,1', qos=0, retain=False)
    client.publish('lcd/write', str(l.atmosphere['humidity'] + '%'), qos=0, retain=False)

    # Write Cond
    client.publish('lcd/move', '0,2', qos=0, retain=False)
    client.publish('lcd/write', 'Cond:', qos=0, retain=False)
    client.publish('lcd/move', '5,2', qos=0, retain=False)
    client.publish('lcd/write', '               ', qos=0, retain=False)  # Clear line for 20 char wide LCD
    client.publish('lcd/move', '5,2', qos=0, retain=False)
    client.publish('lcd/write', str(l.condition.text), qos=0, retain=False)

    # Write Cond
    client.publish('lcd/move', '0,3', qos=0, retain=False)
    client.publish('lcd/write', 'Tmro:', qos=0, retain=False)
    client.publish('lcd/move', '5,3', qos=0, retain=False)
    client.publish('lcd/write', '               ', qos=0, retain=False)  # Clear line for 20 char wide LCD
    client.publish('lcd/move', '5,3', qos=0, retain=False)
    client.publish('lcd/write', str(l.forecast[1].text), qos=0, retain=False)


def write_time(now):
    if now.hour > 13:
        hour = now.hour - 12
        am_pm = ' Pm'
    else:
        hour = now.hour
        am_pm = ' Am'

    if now.minute < 10:
        minute = '0' + str(now.minute)
    else:
        minute = now.minute

    time = str(hour) + ":" + str(minute) + am_pm

    client.publish('lcd/move', '0,0', qos=0, retain=False)
    client.publish('lcd/write', 'Time:', qos=0, retain=False)
    client.publish('lcd/move', '5,0', qos=0, retain=False)
    client.publish('lcd/write', '               ', qos=0, retain=False)
    client.publish('lcd/move', '5,0', qos=0, retain=False)
    client.publish('lcd/write', time + '   ' + str(now.month) + '/' + str(now.day), qos=0, retain=False)


def main():
    client.publish('lcd/clear', qos=0, retain=False)
    while True:
        now = datetime.datetime.now(pytz.timezone(mqtt_creds_server.pytz_timezone))
        if now.second == 0:
            write_time(now)
            write_weather()
            if now.hour > 22 or now.hour < 7: # Turn off backlight when its night time
                client.publish('lcd/backlight', '1', qos=0, retain=False)
            else:
                client.publish('lcd/backlight', '0', qos=0, retain=False)
            sleep(2)
        sleep(.1)  # Prevent 100% CPU Usage


if __name__ == "__main__":
    main()
