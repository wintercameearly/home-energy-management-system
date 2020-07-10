 Import standard python modules.
import json
import random
import sys
import time
import serial
import datetime
import time
import jwt
import paho.mqtt.client as mqtt
import RPi.GPIO as io
import base64

io.setmode(io.BCM)

# Setup for Google Cloud IoT Core
ssl_private_key_filepath = '/home/pi/jwtRS256.key'
ssl_algorithm = 'RS256'
root_cert_filepath = '/home/pi/roots.pem'
project_id = 'raspberry-connector'
gcp_location = 'asia-east1'
registry_id = 'rasberry-pi-registry'
device_id = 'raspi-device'
cur_time = datetime.datetime.utcnow()
_CLIENT_ID = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id, gcp_location, registry_id,
                                                                        device_id)
_MQTT_TOPIC = '/devices/{}/events'.format(device_id)
#_MQTT_TOPIC = 'projects/raspberry-connector/topics/data'
# For serial communication
serial1 = serial.Serial('/dev/ttyAMA0', 38400)

# use software pin numbering
relay1_pin = 22
relay2_pin = 23
relay3_pin = 24

# configure the pins to be used as outputs
io.setup(relay1_pin, io.OUT)
io.setup(relay2_pin, io.OUT)
io.setup(relay3_pin, io.OUT)

# set initial pin states to off
io.output(relay1_pin, False)
io.output(relay2_pin, False)
io.output(relay3_pin, False)

relay1_status = '0'
relay2_status = '0'
relay3_status = '0'

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'aio_fBwP163pnajwp1A7xWFdpkVbmjHk'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'nifemibam'


# Create a jwt connection for Cloud IoT core
def create_jwt():
    token = {
        'iat': cur_time,
        'exp': cur_time + datetime.timedelta(minutes=60),
        'aud': project_id
    }

    with open(ssl_private_key_filepath, 'r') as f:
        private_key = f.read()
        print(private_key)
    return jwt.encode(token, private_key, ssl_algorithm)


# Setup client for IoT Core
client1 = mqtt.Client(client_id=_CLIENT_ID)
# authorization is handled purely with JWT, no user/pass, so username can be wh$
client1.username_pw_set(
    username='unused',
    password=create_jwt())


# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for Test changes...')
    # Subscribe to changes on all the feeds
    client.subscribe('entire-home-power')
    client.subscribe('relay-1')
    client.subscribe('relay-2')
    client.subscribe('relay-3')
    client.subscribe('current')


def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    if feed_id == 'relay-1':
        relay1_status = payload
        print(relay1_status)
        if relay1_status == '0':
            print("Switching Relay 1 Off")
            io.output(relay1_pin, False)
        elif relay1_status == '1':
            print("Switching Relay 1 On")
            io.output(relay1_pin, True)

    if feed_id == 'relay-2':
        relay2_status = payload

        if relay2_status == '0':
            print("Switching Relay 2 Off")
            io.output(relay2_pin, False)
        elif relay2_status == '1':
            print("Switching Relay 2 On")
            io.output(relay2_pin, True)

    if feed_id == 'relay-3':
        relay3_status = payload
        if relay3_status == '0':
            print("Switching Relay 3 Off")
            io.output(relay3_pin, False)
        elif relay3_status == '1':
            print("Switching Relay 3 On")
            io.output(relay3_pin, True)

# Google cloud callback functions 
def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))


def on_connect(unusued_client, unused_userdata, unused_flags, rc):
    print('on_connect', error_str(rc))


def on_publish(unused_client, unused_userdata, unused_mid):
    print('on_publish')


# Create an MQTT client instance for Adafruit.IO
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message

# Google cloud callback functions
client1.on_connect = on_connect
client1.on_publish = on_publish

# Connect to the Adafruit IO server.
client.connect()

# Now the program needs to use a client loop function to ensure messages are
# sent and received.  There are a few options for driving the message loop,
# depending on what your program needs to do.

# The first option is to run a thread in the background so you can continue
# doing things in your program.

client.loop_background()
client1.loop_start()

# Gcloud connection
client1.tls_set(ca_certs=root_cert_filepath)  # Replace this with 3rd party cert $
client1.connect('mqtt.googleapis.com', 8883)

# Now send new values every 10 seconds.
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
ser = serial.Serial('/dev/ttyAMA0', 38400)
timestamp_list = []
power_list = []
while True:
    power = 0
    
    response = ser.readline()
    response = response[:-2]

    Z = response.split(" ")
    value = Z[1]
    current = float(value) / 230
    print('Publishing {0} to DemoFeed.'.format(value))
    client.publish('entire-home-power', value)
    #client.publish('current', current)
    
    cur_power = float(Z[1])
    #if cur_power == power:
     #   time.sleep(1)
      #  continue

    #power = int(round(cur_power))
    power = cur_power
    timestamp = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print(power)
    power_list.append(power)
    timestamp_list.append(timestamp)
    print(len(power_list))
    if len(power_list) == 20:
        #payload = '{{"timestamp":{},"power":{}, "device_id":"fy-raspi"}}'.format(timestamp_list,power_list)
        payload = {"timestamp":timestamp_list,"power":power_list,"device_id":"fy-raspi"}
        payload = json.dumps(payload)
        d = datetime.datetime.utcnow()
        d = d.isoformat("T")+"Z"
        #payload = base64.b64encode(payload)
        sending_info = {"data": payload,
        "attributes": {
        'deviceId': 'raspi-device',
        'deviceNumId': '3332544173922627',
        'deviceRegistryId': 'rasberry-pi-registry',
        'deviceRegistryLocation': 'asia-east1',
        },
        "messageId": "122345677777",
        "publishTime": d
        }
        # sending_info = {'message':{'attributes':{'deviceId':'raspi-device','deviceNumId':'3332544173922627','deviceRegistryId': 'rasberry-pi-registry','deviceRegistryLocation':'asia-east1','projectId':'raspberry-connector','subFolder':$
        # sending_info = json.dumps(sending_info).encode('utf-8')
        client1.publish(_MQTT_TOPIC, payload, qos=1)
        print("{}\n".format(sending_info))
        del power_list[:]
        del timestamp_list[:] 
    #payload = '{{"ts": {},"power": {} }}'.format(int(time.time()), power)
    #client1.publish(_MQTT_TOPIC, payload, qos=1)
    #print("{}\n".format(payload))
    time.sleep(3)
    # client1.loop_stop()
