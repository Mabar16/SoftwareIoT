from __future__ import print_function # Python 2/3 compatibility
import paho.mqtt.client as mqtt
import time
import json
import boto3

dynamodb = boto3.resource('dynamodb',
    region_name='eu-central-1',
    aws_access_key_id='AKIAJLFH3N6PIXRQOY4Q',
    aws_secret_access_key='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',
)
def writeToTempTable(payload, timestamp):
    table = dynamodb.Table('CleverCupTemperature')
    temp = payload['temperature']#.decode("utf-8")
    device = payload['deviceid']
    table.put_item(
        Item={
            'id': timestamp,
            'deviceid': device,
            'temperature': str(temp)

        }
    )

def writeToLocationTable(payload, timestamp):
    
    table = dynamodb.Table('CleverCupLocation')
    lat = payload['latitude']#.decode("utf-8")
    long = payload['longitude']#.decode("utf-8")
    device = payload['deviceid']    
    table.put_item(
        Item={
            'id': timestamp,
            'device': device,
            'lat': lat,
            'long': long
    
        }
    )
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("clevercup/temperature")
    client.subscribe("clevercup/geolocation")

def decodeJson(payload):
    jsons = payload.decode("utf8")
    payloadDict = json.loads(jsons)
    return payloadDict

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    timestamp = time.time_ns()
    if ('temperature' in msg.topic):
        payloadDict = decodeJson(msg.payload)
        writeToTempTable(payloadDict, timestamp)
    if ('geolocation' in msg.topic):
        payloadDict = decodeJson(msg.payload)
        writeToLocationTable(payloadDict, timestamp)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("3.126.242.230", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()