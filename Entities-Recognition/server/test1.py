import rdflib
from rdflib import Graph, plugin
import rdflib_jsonld
import json


g = rdflib.Graph()
result = g.parse("Emancipada_final.rdf")
palabra = "emancipada"
query =  'SELECT ?s ?p ?o  WHERE { ?s ?p ?o .FILTER regex(str(?s), "%s") .}'%(palabra)
# Grab a list of all of the Predicates in the graph
# For each item in the predicates generator, print it out

# for subject,predicate,obj in g:
    # sujeto = subject.split("/")
    # predicado = predicate.split("/")
    # objeto = obj.split("/")
    # print(sujeto[-1])
    # print(subject)
    # print(obj)
    # print(predicate," ------- " , obj)
data={}
for row in g.query(query):
    sujeto = row.s.split("/")
    predicado = row.p.split("/")
    objeto = row.o.split("/")
    data[predicado[-1]] = objeto[-1]
    # print(sujeto[-1])

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
