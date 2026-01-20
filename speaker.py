#!/usr/bin/python3

"""Handle all MQTT messages and write details to mongo database
"""


import paho.mqtt.client as mqtt
import signal
from logging_config import LOG_CONFIG
import logging
from logging.config import dictConfig
import sys
import json
from settings import mosquito as mqtt_settings
from piper_voice import PiperJenny
#from gpiozero import Button
import RPi.GPIO as GPIO
from time import sleep
#import board



BUTTON_PIN = 22
BUTTON_LED_PIN = 27

dictConfig(LOG_CONFIG)

logger = logging.getLogger("server")

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"mars-speech-handler")


pv = PiperJenny()

#button = Button(22, pull_up=True, bounce_time=0.1)

repeat = True


def clean_up():
    mqtt_client.disconnect()
    mqtt_client.loop_stop()
    logger.info("*** Ending ***")


def signal_term_handler(signal, frame):
    clean_up()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)    
    
        
def on_connect(client, userdata, flags, rc, properties=None):
    logger.info("Connection {}".format(rc))
    if rc == 0:
        client.subscribe(f"{mqtt_settings['base_topic']}/talk")


def on_disconnect(client, userdata, flags, rc, properties=None):
    logger.info("disconnect {}".format(rc))



def on_subscribe(mqtt_client, obj, mid, granted_qos, properties=None):
    logger.info("Subscribed: {} {}".format(mid, granted_qos))



def on_log(mqtt_client, obj, level, string, properties=None):
    logger.info("Log: {}".format(string))


def handle_speak(mqtt_client, userdata, message):
    """Handle MQTT status.
    update device record with device status (creates if not already exists)
    Args:
        mqtt_client (_type_): _description_
        userdata (_type_): _description_
        message (Object): MQTT message object
    """
    try:
        global repeat
        data = json.loads(message.payload.decode("utf-8"))
        logger.debug(data)
        PROCESS_INTERVAL = 15
        # todo check repeat is valid
        repeat = data["repeat"]
        #pv.say(data["text"])
        GPIO.output(BUTTON_LED_PIN,GPIO.HIGH)
        while repeat:
            pv.say(data["text"])
            logger.debug("starting to sleep")
            for _ in range(PROCESS_INTERVAL):
                if not repeat:
                    break
                sleep(1)
            #sleep(15)            
    except KeyError as ex:
        logger.error(f"Status: KeyError: {ex}" ,exc_info=True)
    except Exception as ex:
        logger.error(f"Status: Other Error: {ex}" ,exc_info=True)


def button_press(btn):
    try:
        logger.debug("Button Pressed")
        global repeat
        GPIO.output(BUTTON_LED_PIN,GPIO.LOW)      
        repeat = False
        # publish.single(f"sound/button/", json.dumps({"switch": b}), hostname=BROKER_ADDRESS, qos=0)
        mqtt_client.publish("sound/button", json.dumps({"switch": 1}), qos=2)
    except Exception as ex:
        logger.error(f"Callback - {ex}",exc_info=True)



def start_mqtt_client():
    try:
        logger.info(f"*** Staring with config {mqtt_settings['name']} ***")
        mqtt_client.on_connect = on_connect
        mqtt_client.on_disconnect = on_disconnect
        mqtt_client.on_subscribe = on_subscribe
        mqtt_client.message_callback_add(f"{mqtt_settings['base_topic']}/talk"
                                         , handle_speak)
        mqtt_client.will_set("status/server/disconnect", json.dumps({}))
        # enable TLS for secure connection - required for hivemq
        if mqtt_settings['ssl'] == True:
            mqtt_client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        mqtt_client.username_pw_set(mqtt_settings['user'], password=mqtt_settings['pw']) 
        mqtt_client.connect_async(mqtt_settings['server'], port=mqtt_settings['port'])
        print("Waiting....")   
        mqtt_client.loop_forever()
    except KeyboardInterrupt:
        clean_up()
    except Exception as ex:
        logger.error(f"main exception {ex}", exc_info=True)
        clean_up()

def setup_gpio():
    """Initialize GPIO settings"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, 
                         callback=button_press, bouncetime=300)
    GPIO.setup(BUTTON_LED_PIN,GPIO.OUT)

if __name__ == '__main__':
    setup_gpio()
    start_mqtt_client() 
