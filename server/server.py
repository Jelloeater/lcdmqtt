__author__ = 'Jesse'

import paho.mqtt.client as mqtt
import mqtt_creds
import datetime
from time import sleep


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(mqtt_creds.username, mqtt_creds.password)
client.connect(mqtt_creds.server, 1883, 60)


# Write_headers
client.publish('lcd/clear', qos=0, retain=False)
client.publish('lcd/move', '0,0', qos=0, retain=False)
client.publish('lcd/write', 'Time:', qos=0, retain=False)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()

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

    client.publish('lcd/move', '5,0', qos=0, retain=False)
    client.publish('lcd/write', time, qos=0, retain=False)


while True:
    now = datetime.datetime.now()
    if now.second == 0:
        write_time(now)
        sleep(2)
    sleep(.1)  # Prevent 100% CPU Usage
