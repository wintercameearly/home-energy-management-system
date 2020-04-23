import serial
ser = serial.Serial('/dev/ttyAMA0', 38400)

# Import standard python modules.
import random
import sys
import time

response = ser.readline()

response = response[:-2]

Z = response.split(" ")

import RPi.GPIO as io
io.setmode(io.BCM)

#use software pin numbering
relay1_pin = 22
relay2_pin = 23
relay3_pin = 24

#configure the pins to be used as outputs
io.setup(relay1_pin, io.OUT)
io.setup(relay2_pin, io.OUT)
io.setup(relay3_pin, io.OUT)

#set inital pin states to off
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
ADAFRUIT_IO_KEY = ''

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = ''


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
            io.output(relay1_pin,True)

    if feed_id == 'relay-2':
        relay2_status = payload

        if relay2_status == '0':
            print("Switching Relay 2 Off")
            io.output(relay2_pin, False)
        elif relay2_status == '1':
            print("Switching Relay 2 On")
            io.output(relay2_pin,True)

    if feed_id == 'relay-3':
        relay3_status = payload
        if relay3_status == '0':
            print("Switching Relay 3 Off")
            io.output(relay3_pin, False)
        elif relay3_status == '1':
            print("Switching Relay 3 On")
            io.output(relay3_pin,True)


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message = message

# Connect to the Adafruit IO server.
client.connect()

# Now the program needs to use a client loop function to ensure messages are
# sent and received.  There are a few options for driving the message loop,
# depending on what your program needs to do.

# The first option is to run a thread in the background so you can continue
# doing things in your program.
client.loop_background()
# Now send new values every 10 seconds.
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
while True:
    value = Z[1]       
    current = value/230
    print('Publishing {0} to DemoFeed.'.format(value))
    client.publish('entire-home-power', value)
    c;eint.publish('current', current)
    time.sleep(7)

# Another option is to pump the message loop yourself by periodically calling
# the client loop function.  Notice how the loop below changes to call loop
# continuously while still sending a new message every 10 seconds.  This is a
# good option if you don't want to or can't have a thread pumping the message
# loop in the background.
#last = 0
#print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
#while True:
#   # Explicitly pump the message loop.
#   client.loop()
#   # Send a new message every 10 seconds.
#   if (time.time() - last) >= 10.0:
#       value = random.randint(0, 100)
#       print('Publishing {0} to DemoFeed.'.format(value))
#       client.publish('DemoFeed', value)
#       last = time.time()

# The last option is to just call loop_blocking.  This will run a message loop
# forever, so your program will not get past the loop_blocking call.  This is
# good for simple programs which only listen to events.  For more complex programs
# you probably need to have a background thread loop or explicit message loop like
# the two previous examples above.
#client.loop_blocking()
