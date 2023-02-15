from rdflib import Graph, Namespace

# Load the OWL ontology into an rdflib Graph object
g = Graph()
g.parse("./teste.xml")

# Define the RDF namespaces used in the OWL ontology
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")

# Query the rdflib Graph for all RDFS labels in the ontology
query = """
SELECT ?label
WHERE {
  ?subject rdfs:label ?label .
}
"""
labels = g.query(query, initNs={"rdfs": RDFS})

# Print out the labels
for label in labels:
    print(label[0])