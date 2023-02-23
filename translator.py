from rdflib import Graph, Namespace

# Prompt the user to enter the path to the OWL ontology file
owl_file_path = input("Enter the path to your OWL ontology file: ")

# Load the OWL ontology into an rdflib Graph object
g = Graph()
g.parse(owl_file_path)

# Define the RDF namespaces used in the OWL ontology
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")

# Query the rdflib Graph for all items and their associated labels
query = """
SELECT ?item ?label
WHERE {
  {?item rdfs:label ?label}
  UNION
  {?item rdf:type owl:Class}
  UNION
  {?item rdf:type owl:ObjectProperty}
  UNION
  {?item rdf:type owl:DatatypeProperty}
  UNION
  {?item rdf:type owl:AnnotationProperty}
  FILTER(lang(?label) = "" || langMatches(lang(?label), "*"))
}
"""
labels = g.query(query, initNs={"rdf": RDF, "rdfs": RDFS, "owl": OWL})

# Group the labels by item using a dictionary
label_dict = {}
for label in labels:
    item_uri = label[0].toPython()
    lang = label[1].language
    if item_uri not in label_dict:
        label_dict[item_uri] = {}
    if lang not in label_dict[item_uri]:
        label_dict[item_uri][lang] = []
    label_dict[item_uri][lang].append(label[1])

# Print out the labels by item
for item_uri, labels_by_lang in label_dict.items():
    print(f"Item {item_uri}:")
    for lang, labels in labels_by_lang.items():
        print(f"  {lang}:")
        for label in labels:
            print(f"    {label}")
