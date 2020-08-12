import base64
import json
from datetime import datetime
import logging
import os
from Adafruit_IO import Client, Feed, Data, RequestError
import datetime

ADAFRUIT_IO_KEY = os.environ.get('adafruit_key')

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = os.environ.get('adafruit_username')

last_send_time = 0


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    print("Execution Starting")
    pubsub_message = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    time_elapsed = 240
    limit = float(120)
    print("Checking Time limit")
    print(time_elapsed)
    if time_elapsed > limit:
        print("Limit exceeded, connecting to twillio client")
        prob_list = pubsub_message['probs']
        appliances = ["treadmill", "washing machine", "dishwasher", "microwave", "microwave", "kettle", " ", " "]
        active_appliances = []
        print("Checking probabilities of appliances")
        for prob in prob_list:
            if prob > 0.2:
                index = prob_list.index(prob)
                device_name = appliances[index]
                active_appliances.append(device_name)
                print("Appliance {} detected".format(device_name))
    if active_appliances:
        # Create an instance of the REST client.
        aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
        devices = aio.feeds('devices')
        # aio.send_data(devices.key, active_appliances.index(appliance))
        # for appliance in active_appliances:
        #     aio.send_data(devices.key, appliance)
        #     print("Sending data to adafruit feed")
        #     print("Data Sent")
        str = " "
        data = str.join(active_appliances)
        aio.send_data(devices.key, data)
        print("Sent")





