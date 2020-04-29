const express = require('express')
const mqtt = require('mqtt') //npm install mqtt -g
const app = express()
const port = 3000

const { Client } = require('pg')

var secret = require('./secret');

const dbclient = new Client({
    user: 'vibar',
    host: 'clevercupdb.ckz9vj0cvxvl.eu-central-1.rds.amazonaws.com',
    database: 'CleverCupDb',
    password: secret.dbpassword(),
    port: 5432,
})
dbclient.connect()

var deviceLocations = {}
app.use(express.static('static'))


app.get('/publishComfortRange', (req, res) => {
    try {

        publishComfortRange(req.query.deviceID, req.query.tempMin, req.query.tempMax)
        res.send("OK")
    } catch (error) {
        console.error(error);
    }
})

app.get('/getDevices', (req, result) => {
    try {

        dbclient.query('select distinct devicename from temperature', (err, res) => {
            try {


                if (err)
                    console.log(err)
                names = res.rows.map(r => r.devicename)

                result.send(names)
            } catch (error) {
                console.error(error);
            }
        })
    } catch (error) {
        console.error(error);
    }
})

app.get('/getCupLocation', (req, res) => {
    try {
        location = findCup(req.query.deviceID)
        console.log(req.query.deviceID + "  " + location)
        res.send(location)
    } catch (error) {
        console.error(error);
    }
})

app.get("/getAllTemperatureData", (requst, result) => {
    try {
        dbclient.query('select * from temperature where "devicename" = \'' + requst.query.deviceID + '\' order by pycomtime', (err, res) => {
            if (err)
                console.log(err)
            console.log(res.rowCount)

            result.send(res)
        })
    } catch (error) {
        console.error(error);
    }
})


app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))

var client = mqtt.connect("mqtt://3.127.128.243")

client.on("connect", () => {
    console.log("CONNEC")
    //
})

client.on("disconnect", () => {
    console.error("Disconnected from MQTT Broker")
    //
})

client.on("offline", () => {
    console.error("I dont have internet!!!")
    //
})

client.on("close", () => {
    console.error("Emitted after a disconnection ( why did we disconnec???)")
    //
})

client.on("error", () => {
    console.error("Cannot Connec!!!!")
    // One of:
    // ECONNREFUSED
    // ECONNRESET
    // EADDRINUSE
    // ENOTFOUND
})



client.subscribe("clevercup/location")

client.on("message", (topic, message) => {
    try {
        // console.log(topic+ "    " + message)
        if (topic === 'clevercup/location') {
            payload = JSON.parse(message)
            devicename = payload["deviceid"]
            location = { lat: payload.latitude, lon: payload.longitude }
            console.log(devicename + "    " + JSON.stringify(location))
            deviceLocations[devicename] = location
        }
    } catch (error) {
        console.error(error);
    }
})

function publish(topic, message) {
    try {
        console.log(topic)
        console.log(message)
        client.publish(topic, message, console.log)
    } catch (error) {
        console.error(error);
    }
}

function publishComfortRange(deviceID, tempMin, tempMax) {
    try {
        console.log("publishing! " + tempMin + "   " + tempMax)

        topic = "device/" + deviceID + "/comfortrange/updates"
        message =
        {
            'device': deviceID,
            'newmin': parseInt(tempMin, 10),
            'newmax': parseInt(tempMax, 10)
        }
        msgstring = JSON.stringify(message)
        publish(topic, msgstring)
    } catch (error) {
        console.error(error);
    }
}

function findCup(deviceID) {
    return deviceLocations[deviceID]
}

