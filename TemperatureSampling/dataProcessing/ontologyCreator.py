from wrapping import *

TTL_FILENAME = '.\\var\\mappingOntology.ttl'

g = model()
print("initial file read")

#Types:
g.add((N['Device'], OWL["subClassOf"], OWL["Class"]))
g.add((N['Calibration'], OWL["subClassOf"], OWL["Class"]))
g.add((N['Function'], OWL["subClassOf"], OWL["Class"]))
g.add((N['LinearFunction'], OWL["subClassOf"], N['Function']))

#Relationships:
g.add((N['hasCalibration'], RDF["type"], OWL["ObjectProperty"]))
g.add((N['hasFunction'], RDF["type"], OWL["ObjectProperty"]))
g.add((N['aParameterValue'], RDF["type"], OWL["DataProperty"]))
g.add((N['bParameterValue'], RDF["type"], OWL["DataProperty"]))
g.add((N['intervalStart'], RDF["type"], OWL["DataProperty"]))
g.add((N['intervalEnd'], RDF["type"], OWL["DataProperty"]))
g.add((N['minValue'], RDF["type"], OWL["DataProperty"]))
g.add((N['maxValue'], RDF["type"], OWL["DataProperty"]))
g.add((N['avgValue'], RDF["type"], OWL["DataProperty"]))

# Restrictions:
# A device has a calibration 
g.add((N['hasCalibration'], RDFS.range, N['Calibration']))# it must be type calibration

def addCardinalityRestriction(onProperty, onType, min, max=None):
    r= N[onProperty+"CardinalityRestriction"]
    g.add((r, RDF.type, OWL['Restriction']))
    g.add((r, OWL.onProperty, N[onProperty]))
    if max is not None:
        g.add((r, OWL.maxCardinality, Literal(max)))
    if min is not None:
        g.add((r, OWL.minCardinality, Literal(min)))
    g.add((N[onType], OWL.equivalentClass, r))

addCardinalityRestriction("hasCalibration","Device", 1, 1)

g.add((N['hasFunction'], RDFS.range, N['Function']))# it must be type func

addCardinalityRestriction("hasFunction","Calibration", 1)



# A calibration is usefull with one set of settings (i.e., one attenuationValue) (not modelled)
# And a calibration has many functions that perform a mapping for a certain interval

# A function has exactly one of each [istart, iend, min, max, avg]
# A LINEARfunction has exactly one of each [a, b]
g.add((N['aParameterValue'], RDFS.range, OWL["float"]))# it must be type float
addCardinalityRestriction("aParameterValue","LinearFunction", 1,1)
g.add((N['bParameterValue'], RDFS.range, OWL["float"]))# it must be type float
addCardinalityRestriction("bParameterValue","LinearFunction", 1,1)
g.add((N['intervalStart'], RDFS.range, OWL["float"]))# it must be type float
addCardinalityRestriction("intervalStart","Function", 1,1)
g.add((N['intervalEnd'], RDFS.range, OWL["float"]))# it must be type float
addCardinalityRestriction("intervalEnd","Function", 1,1)
g.add((N['minValue'], RDFS.range, OWL["float"]))# it must be type float
addCardinalityRestriction("minValue","Function", 1,1)
g.add((N['maxValue'], RDFS.range, OWL["float"]))# it must be type float
addCardinalityRestriction("maxValue","Function", 1,1)
g.add((N['avgValue'], RDFS.range, OWL["float"]))# it must be type float
addCardinalityRestriction("avgValue","Function", 1,1)



# # Demo, sketch, not part of ontology:
# f = N["Function"]
# (f, N["aParameterValue"], 2)
# (f, N["bParameterValue"], -58) # f(x) = 2*x -58
# (f, N["intervalStart"], 30)
# (f, N["intervalEnd"], 35)
# (f, N["minValue"], 31)#f(30))
# (f, N["maxValue"], 42)#f(35))
# (f, N["avgValue"], 40)


print("serializing")
g.serialize(TTL_FILENAME, 'turtle')
print("serialized")