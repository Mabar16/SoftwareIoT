#!/usr/bin/env python3

from wrapping import *

TTL_FILENAME = '.\\var\\temperatureMapping.ttl'

g = model()
print("initial file read")
###############################################################################
################################################################### calibration ####

device = N['/device']
g.add((device, RDF.type, TYPES["Device"]))

###############################################################################
################################################################# device ####

sensor = N['/device/temperaturesensor']
g.add((device, RELATIONS.has, sensor))

###############################################################################
################################################################### calibration ####

calibration = N['/device/temperaturesensor/calibration']
g.add((sensor, RELATIONS.has, calibration))

###############################################################################
############################################################# room mapping ####

distribution = {
    '0': {
        'min': '37',
        'max': '37',
        'avg': '37',
        'start': '37',
        'end': '37',
    },
    '1': {
        'min': '38',
        'max': '38',
        'avg': '38',
        'start': '38',
        'end': '38',
    },
}

###############################################################################
#################################################################### rooms ####

distributionMap = {}
for rownumber in distribution:
    data = distribution[rownumber]
    mapping = N['/device/temperaturesensor/calibration/mappings/%s' % rownumber]
    g.add((mapping, RDF.type, TYPES['TemperatureDistribution']))
    g.add((mapping, ATTRIBUTES.label, Literal(rownumber)))
    g.add((mapping, ATTRIBUTES.min, Literal(data["min"])))
    g.add((mapping, ATTRIBUTES.max, Literal(data["max"])))
    g.add((mapping, ATTRIBUTES.avg, Literal(data["avg"])))
    g.add((mapping, ATTRIBUTES.start, Literal(data["start"])))
    g.add((mapping, ATTRIBUTES.end, Literal(data["end"])))
    g.add((calibration, RELATIONS.has, mapping))
    distributionMap[rownumber] = mapping


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
SELECT DISTINCT ?min ?max ?calibration
WHERE {
    ?calibration   rdf:type                types:TemperatureDistribution .
    ?calibration   attributes:label        ?rowNumber .
    ?calibration   attributes:min          ?min .
    ?calibration   attributes:max          ?max .
        
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
