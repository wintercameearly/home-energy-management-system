# Cloud Based IoT Energy Management System
An Energy Management System built for the purpose of improving Home Enegery Usage Efficiency.

This system was built, Cloud Technologies and systems to enable consistent, location-independent access to energy information.

LIVE DEMO : https://www.youtube.com/watch?v=67l0wjL0xx0&t=7s


![Flowchart](https://github.com/wintercameearly/undergrad_proj/blob/master/cronos.jpeg)
mqtttest.py is the mqtt client for sending data to adafruit.io and controlling the devices connected to it 


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

GCP recoeves readings from RaspberryPi through Cloud IoT core and Pub/Sub
GCP hosts an RNN-LSTM Model on Cloud AI Platform, adapted from (https://github.com/GoogleCloudPlatform/professional-services/tree/master/examples/e2e-home-appliance-status-monitoring
) to carry out Energy Disaggregation.
Responses from the Model are sent to Adafruit.io via its HTTP API on a Feed , and sent as Notifications to users via the Twillio API with the use of Google Cloud Functions 

Also added some features with IFTTT for Voice Control and a diluted form of Demand Response


This work is possible very much due to the examples provided by Google , Very Grateful to them !
