#!/usr/bin/env python3

from wrapping import *
import csv

TTL_FILENAME = '.\\var\\temperatureMapping.ttl'

g = model()
print("initial file read")
###############################################################################
################################################################### calibration ####

device = N['/myFirstDevice']
g.add((device, RDF.type, N["Device"]))


###############################################################################
################################################################### calibration ####

calibration = N['/calibrationOne']
g.add((calibration, RDF.type, N['Calibration']))
#g.add((calibration, ATTRIBUTES.attenuation, Literal('1')))

###############################################################################
############################################################# room mapping ####


distribution = {}

mapping_ = {}
with open('mapping.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count +=1
        elif row[5] == "":
            pass
        else:

            #print(line_count)
            mapping_['start'] = float(row[0])
            mapping_['end'] = float(row[1])
            mapping_['min'] = float(row[2])
            mapping_['max'] = float(row[3])
            mapping_['avg'] = float(row[4])
            mapping_['a'] = float(row[5])
            mapping_['b'] = float(row[6])
          #  print(mapping_['avg'])
            distribution[mapping_['start']] = mapping_
            mapping_ = {}

###############################################################################
#################################################################### rooms ####

distributionMap = {}
for rownumber in distribution:
    data = distribution[rownumber]

    function = N['Function'+str(rownumber)]
    g.add((function,RDF.Type,N["LinearFunction"]))
    g.add((function,N.intervalStart, Literal(data["start"])))
    g.add((function,N.intervalEnd, Literal(data["end"])))
    g.add((function,N.minValue, Literal(data["min"])))
    g.add((function,N.maxValue, Literal(data["max"])))
    g.add((function,N.avgValue, Literal(data["avg"])))
    g.add((function,N.aParameterValue, Literal(data["a"])))
    g.add((function,N.bParameterValue, Literal(data["b"])))

    g.add((calibration, N.hasFunction, function))
    distributionMap[rownumber] = function


###############################################################################
########################## store-load cycle to simulate applications split ####
print("serializing")
g.serialize(TTL_FILENAME, 'turtle')
print("serialized")


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
