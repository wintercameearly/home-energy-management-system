# Cloud Based IoT Energy Management System
An Energy Management System built for the purpose of improving Home Enegery Usage Efficiency.

This system was built using Cloud Technologies and systems to enable consistent, location-independent access to energy information.

LIVE DEMO : https://www.youtube.com/watch?v=67l0wjL0xx0&t=7s


![Flowchart](https://github.com/wintercameearly/undergrad_proj/blob/master/cronos.jpeg)



## Features 

1. Monitoring of Entire Home Energy Usage via Online Dashboard
2. Control of Appliances Remotely
3. Disaggregation and Monitoring/Recognition of Individual Appliances based on Gross Power reading
4. Notifications on Energy Usage 

## Technologies Used
This work was written in Python
It utilizes a Current Transformer Clamp and the RPICT3T1 for CURRENT measurement and a ZMPT101B Voltage Transformer with the ESP8266 for Voltage Measurement. 

Both of these are connected to a Raspberry Pi over serial to compute into power and send *almost* Real-Time readings to Google Cloud Platform and adafruit.io

Adafruit.io Dashboard shows the readings ot the Entire Home Power Usage 

GCP recieves readings from RaspberryPi through Cloud IoT core and Pub/Sub
GCP hosts an RNN-LSTM Model on Cloud AI Platform, adapted from (https://github.com/GoogleCloudPlatform/professional-services/tree/master/examples/e2e-home-appliance-status-monitoring
) to carry out Energy Disaggregation.
Responses from the Model are sent to Adafruit.io via its HTTP API on a Feed , and sent as Notifications to users via the Twillio API with the use of Google Cloud Functions 

Also added some features with IFTTT for Voice Control and a diluted form of Demand Response

## Scripts

1. communication.py : This is the script responsible for sending information to GCP and Adafruit.io. Please note there is some authentication and configuration to be done to get API keys, JWT authentication and the likes. It runs on the Raspberry Pi

2. cloudfunctions : this folder holds the two cloud functions responsible for sending to adafruit.io(adafruit.py) and twillio(sms.py)

3. ml : This folder hosts the Tensorflow Model, start scripts and yaml files for GCP AI Platform  to enable deployment of the model.

4. gatewayservice : This folder holds the gateway service responsible for calling the deployed Model endpoint, pushing responses to PubSub and storing data in BigQuery.


This work is possible very much due to the examples provided by Google , Very Grateful to them !
