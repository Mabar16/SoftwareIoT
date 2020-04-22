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

var deviceLocations =
{
    'vicPycom': '',
    'markusPycom': ''
}
app.use(express.static('static'))


app.get('/', (req, res) => res.send('Hello World!'))
app.get('/publishComfortRange', (req, res) => {

    publishComfortRange(req.query.deviceID, req.query.tempMin, req.query.tempMax)
    res.send("OK")
})

app.get('/getDevices', (req,res) => res.send(Object.keys(deviceLocations)))

app.get('/getCupLocation', (req, res) => {

    location = findCup(req.query.deviceID)
    console.log(req.query.deviceID + "  " + location)
    res.send(location)
})

app.get("/getAllTemperatureData", (requst,result)=>{
    dbclient.query('select * from temperature where "devicename" = \''+requst.query.deviceID+'\' order by pycomtime', (err, res) => {
        if(err)
            console.log(err)
        console.log(res.rowCount)
        
        result.send(res)
    })
})


app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))

var client = mqtt.connect("mqtt://3.127.128.243")

client.on("connect", () => {
    console.log("CONNEC")
    //
})

Object.keys(deviceLocations).forEach(devicename=>{

    client.subscribe("device/"+devicename+"/location/update")
})

client.on("message", (topic, message) => {
    // console.log(topic+ "    " + message)
    if (topic.includes("location/update")) {
        payload = JSON.parse(message)
        devicename = topic.split("/")[1]
        location = { lat: payload.latitude, lon: payload.longitude }
        console.log(devicename + "    " + JSON.stringify(location))
        deviceLocations[devicename] = location
    }
})

function publish(topic, message) {
    console.log(topic)
    console.log(message)
    client.publish(topic, message, console.log)
}

function publishComfortRange(deviceID, tempMin, tempMax) {
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
}

function findCup(deviceID) {
    return deviceLocations[deviceID]
}

function placeCupMarker(deviceID, lat, long) {
    L.marker([lat, long]).addTo(mymap).bindPopup("<b>" + deviceID + " is here!</b>.").openPopup();
}