const express = require('express')
const mqtt = require('mqtt') //npm install mqtt -g
const app = express()
const port = 3000

// Load the AWS SDK for Node.js
var AWS = require('aws-sdk');

// Set the region 
AWS.config.update({region: 'eu-central-1'});

var deviceLocations = 
                    {
                        'vicPycom':'',
                        'markusPycom':''
                    }
app.use(express.static('static'))


app.get('/', (req, res) => res.send('Hello World!'))
app.get('/publishComfortRange', (req,res) =>{
    
    publishComfortRange(req.query.deviceID, req.query.tempMin, req.query.tempMax)
    res.send("OK")
} )

app.get('/getCupLocation', (req,res) =>{
    
    location = findCup(req.query.deviceID)
    console.log(location)
    res.send(location)
} )
    

app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))

var client  = mqtt.connect("mqtt://3.126.242.230")

client.on("connect", () =>{
    console.log("CONNEC")
    //
})

client.subscribe("device/vicPycom/location/update")

client.on("message", (topic, message) =>{
   // console.log(topic+ "    " + message)
    if( topic.includes("location/update")){
        payload = JSON.parse(message)
        devicename = topic.split("/")[1]
        location = {lat: payload.latitude, lon: payload.longitude}
        deviceLocations[devicename] = location
    }
})

function publish(topic, message){
    console.log(topic)
    console.log(message)
    client.publish(topic, message, console.log)
}

function publishComfortRange(deviceID, tempMin, tempMax){
    console.log("publishing! " + tempMin + "   " + tempMax)

    topic = "device/"+deviceID+"/comfortrange/updates"
    message = 
                {
                    'device': deviceID,
                    'newmin': parseInt(tempMin, 10),
                    'newmax': parseInt(tempMax, 10)
                }
    msgstring = JSON.stringify(message)
    publish(topic, msgstring)
}

function findCup(deviceID){    
    return deviceLocations[deviceID]
}

function placeCupMarker(deviceID, lat, long){
    L.marker([lat, long]).addTo(mymap).bindPopup("<b>"+deviceID+" is here!</b>.").openPopup();
}