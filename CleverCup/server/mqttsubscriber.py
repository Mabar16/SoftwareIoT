from __future__ import print_function # Python 2/3 compatibility
import paho.mqtt.client as mqtt
import time
import json
import postgresql
import config
import logging

host="clevercupdb.ckz9vj0cvxvl.eu-central-1.rds.amazonaws.com"
port=5432
dbname="CleverCupDb"
user="vibar"
password=config.dbpassword

logging.basicConfig(filename='example.log',level=logging.DEBUG)

db =postgresql.open('pq://'+user+':'+password+'@'+host+':'+str(port)+'/'+dbname+'')

# 
def writeToTempTable(payload, timestamp):
    temp = payload['temperature']#.decode("utf-8")
    device = payload['deviceid']
    pycomtime = payload['pycomtime']

    query = "Insert into temperature (\"value\", \"devicename\",\"pycomtime\") values  ("+str(temp)+", '"+device+"', "+str(pycomtime)+")"
    db.execute(query)

def sanityCheck(payload, timestamp):
    if(payload["pycomtime"] > timestamp):
        logging.warning("TIME ERROR"+ json.dumps(payload))
        return False
    if(payload["temperature"] > 100 or payload["temperature"] < -20):
        logging.warning("TEMPERATURE ERROR"+ json.dumps(payload))
        return False
    return True
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.warning("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("clevercup/temperature")

def decodeJson(payload):
    jsons = payload.decode("utf8")
    payloadDict = json.loads(jsons)
    return payloadDict

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    timestamp = time.time_ns()
    if ('temperature' in msg.topic):
        payloadDict = decodeJson(msg.payload)
        if(sanityCheck(payloadDict, timestamp)):
            writeToTempTable(payloadDict, timestamp)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("3.127.128.243", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()