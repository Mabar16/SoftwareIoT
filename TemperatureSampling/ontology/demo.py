#!/usr/bin/env python3

from wrapping import *

TTL_FILENAME = './var/temperatureMapping.ttl'

g = model()
print("initial file read")
###############################################################################
################################################################# device ####

device = N['/device']
g.add((device, RDF.type, TYPES["Device"]))

###############################################################################
################################################################### measurements ####

# measurements = []
# for measurementId in range(2): #Actually read these from excel file?
#     measurement = N['device/measurements/%u' % measurementId]
#     g.add((measurement, RDF.type, TYPES['TemperatureMeasurement']))
#     g.add((device, RELATIONS.contains, measurement))
#     measurements.append(measurement)

###############################################################################
############################################################# room mapping ####

measurements = {
    '0': {
        'reading': 4095,
        'time-before': '123456789012345',
        'time-after': '123456789012346',
    },
    '1': {
        'reading': 2095,
        'time-before': '123456789012345',
        'time-after': '123456789012346',
    },
    '2': {
        'reading': 3095,
        'time-before': '123456789012345',
        'time-after': '123456789012346',
    },
}

###############################################################################
#################################################################### rooms ####

measurementsMap = {}
for rownumber in measurements:
    data = measurements[rownumber]
    measurement = N['device/measurements/%s' % rownumber]
    g.add((measurement, RDF.type, TYPES['TemperatureMeasurement']))
    g.add((measurement, ATTRIBUTES.label, Literal(rownumber)))
    g.add((measurement, ATTRIBUTES.reading, Literal(data["reading"])))
    g.add((measurement, ATTRIBUTES.timestamp, Literal(data["time-after"])))
    g.add((device, RELATIONS.has, measurement))
    measurementsMap[rownumber] = measurement


###############################################################################
########################## store-load cycle to simulate applications split ####
print("serializing")
g.serialize(TTL_FILENAME, 'turtle')
print("serialized")
del g
g = Graph()
g.parse(TTL_FILENAME, format='turtle')
print("parsed")
###############################################################################
########################################################### dashbard query ####

q_dashboard = \
'''
SELECT DISTINCT ?measurement ?reading ?rowNumber
WHERE {
    ?measurement     rdf:type types:TemperatureMeasurement .
    ?measurement   attributes:label ?rowNumber .
    ?measurement   attributes:reading ?reading .
        
}
'''
pprint(query(g, q_dashboard))

# ###############################################################################
# ######################################################### thermostat query ####

# q_thermostat = \
# '''
# SELECT DISTINCT ?room_name ?sensor_uuid ?setpoint_uuid ?actuator_uuid
# WHERE {
#     ?room     rdf:type/brick:subClassOf* brick:Room .
#     ?sensor   rdf:type/brick:subClassOf* brick:Temperature_Sensor .
#     ?setpoint rdf:type/brick:subClassOf* brick:Temperature_Setpoint .
#     ?actuator rdf:type/brick:subClassOf* brick:Radiator_Valve_Position .
    
#     ?sensor   brick:pointOf ?room .
#     ?setpoint brick:pointOf ?room .
#     ?actuator brick:pointOf ?room .
    
#     ?room     brick:label ?room_name .
#     ?sensor   brick:label ?sensor_uuid .
#     ?setpoint brick:label ?setpoint_uuid .
#     ?actuator brick:label ?actuator_uuid .
# }
# '''
# pprint(query(g, q_thermostat))

# ###############################################################################
# ################################################################### update ####

# q_update = \
# '''
# DELETE {
#     ?actuator brick:label "ec883cad-3235-46d5-a901-7bae169dda0a" .
# }
# WHERE {
#     ?actuator rdf:type/brick:subClassOf* brick:Radiator_Valve_Position .
#     ?actuator brick:label "ec883cad-3235-46d5-a901-7bae169dda0a" .
# }
# '''
# update(g, q_update)

# ###############################################################################
# ################################################## repeat thermostat query ####

# pprint(query(g, q_thermostat))

# ###############################################################################
# ###############################################################################
