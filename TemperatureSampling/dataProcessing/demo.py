
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
SELECT DISTINCT ?fun ?cal ?min ?avg ?max ?a ?b ?funtype
WHERE {{
    ?cal rdf:type   n:Calibration .
    ?cal n:hasFunction ?fun .
    ?fun n:intervalStart ?start . FILTER (?start <= {READING}) .
    ?fun n:intervalEnd ?end . FILTER (?end > {READING}) .
    ?fun n:avgValue ?avg .
    ?fun n:minValue ?min .
    ?fun n:maxValue ?max .
    ?fun n:aParameterValue ?a . 
    ?fun n:bParameterValue ?b . 
    ?fun rdf:type ?funtype .
}}
'''

pprint(query(g, q_dashboard))