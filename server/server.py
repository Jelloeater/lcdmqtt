__author__ = 'Jesse'
import logging

logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)",
                    level=logging.INFO,
                    # filename='autobot.log'  #Logging to file disabled
                    )

import paho.mqtt.client as mqtt
import mqtt_creds_server # Rename mqtt_creds_example and fill in your own info
import datetime
import pytz
from time import sleep
import weather

client = mqtt.Client()
client.username_pw_set(mqtt_creds_server.username, mqtt_creds_server.password)
client.connect(mqtt_creds_server.server, 1883, 60)


def write_weather():
    w = weather.Weather()
    l = w.lookup(mqtt_creds_server.yahoo_world_id)

    client.publish('lcd/move', '0,1', qos=0, retain=False)
    client.publish('lcd/write', 'Temp:' + str(l.condition.temp + 'C ' + l.condition.text), qos=0, retain=False)


def write_time(now):
    if now.hour > 12:
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
    client.publish('lcd/write', 'Time:' + time, qos=0, retain=False)


while True:
    now = datetime.datetime.now(pytz.timezone(mqtt_creds_server.pytz_timezone))
    if now.second == 0:
        client.publish('lcd/clear', qos=0, retain=False)
        write_time(now)
        write_weather()
        sleep(2)
    sleep(.1)  # Prevent 100% CPU Usage
