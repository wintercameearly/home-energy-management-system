import base64
from twilio.rest import Client
import json
from datetime import datetime
import logging
import os

last_send_time = 0


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    print("Execution Starting")
    pubsub_message = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    execution_time = datetime.now()
    global last_send_time
    last_send_time = "2020-07-11 03:47:30"
    last_send_time_obj = datetime.strptime(last_send_time, '%Y-%m-%d %H:%M:%S')
    time_elapsed = (execution_time - last_send_time_obj).total_seconds()
    limit = float(120)
    print("Checking Time limit")
    print(time_elapsed)
    if time_elapsed > limit:
        print("Limit exceeded, connecting to twillio client")
        account_sid = os.environ.get('account_sid')
        auth_token = os.environ.get('account_token')
        client = Client(account_sid, auth_token)
        prob_list = pubsub_message['probs']
        appliances = ["treadmill", "washing machine", "dishwasher", "microwave", " ", "kettle", " ", " "]
        active_appliances = []
        print("Checking probabilities of appliances")
        for prob in prob_list:
            if prob > 0.2:
                index = prob_list.index(prob)
                device_name = appliances[index]
                active_appliances.append(device_name)
                print("Appliance {} detected".format(device_name))
    if active_appliances:
        print("Sending Text Messages")
        Text = "Devices {} are on".format(active_appliances)
        message = client.messages \
            .create(
            body=Text,
            from_='+',
            to='+'
        )
        print("Messages Sent!")
    last_send_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")






