from rdflib import Graph, Namespace, URIRef, Literal
import rdflib
import json
import requests

RDF        = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS       = Namespace('http://www.w3.org/2000/01/rdf-schema#')
OWL        = Namespace('http://www.w3.org/2002/07/owl#')

N = Namespace('http://tempsensor.org/schema#')

def model ():
    g = Graph()
    g.parse('./var/mappingOntology.ttl', format='turtle')
    g.bind('rdf'  , RDF)
    g.bind('rdfs' , RDFS)
    g.bind('owl'  , OWL)
    g.bind('n'    , N)
    
    return g

def query (g, q):
    r = g.query(q)
    return list(map(lambda row: list(row), r))

def update (g, q):
    r = g.update(q)

def pprint (structure):
    pretty = json.dumps(structure, sort_keys=True, indent=4, separators=(',', ': '))
    print(pretty)

