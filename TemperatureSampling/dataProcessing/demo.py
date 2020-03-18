
from wrapping import *
from string import Template

TTL_FILENAME = '.\\var\\temperatureMapping.ttl'

g = Graph()
g.parse(TTL_FILENAME, format='turtle')
print("parsed")
###############################################################################
########################################################### dashbard query ####

READING = 35.7 #Degree C

q_dashboard = \
f'''
SELECT DISTINCT ?fun ?cal ?min ?avg ?max
WHERE {{
    ?cal rdf:type   n:Calibration .
    ?cal n:hasFunction ?fun .
    ?fun n:intervalStart ?start . FILTER (?start <= {READING}) .
    ?fun n:intervalEnd ?end . FILTER (?end > {READING}) .
    ?fun n:avgValue ?avg .
    ?fun n:minValue ?min .
    ?fun n:maxValue ?max .
}}
'''
    # ?fun    n:minValue          ?min .
    # ?fun     n:maxValue           ?max .
    # ?fun    n:avgValue      ?avg.
    # ?calib          rdf:type                n:Calibration .
pprint(query(g, q_dashboard))