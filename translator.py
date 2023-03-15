from rdflib import Graph, Namespace
from textblob import TextBlob

# Prompt the user to enter the path to the OWL ontology file
owl_file_path = input("Enter the path to your OWL ontology file: ")
lang = input("If applicable enter the language of the ontology in ISO 639-1 format (https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes): ")

# Load the OWL ontology into an rdflib Graph object
g = Graph()
g.parse(owl_file_path)

# Define the RDF namespaces used in the OWL ontology
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")

# Query the rdflib Graph for all items and their associated labels
#
query = """
SELECT ?item ?label
WHERE {
  {?item rdfs:label ?label}
  FILTER(lang(?label) = "" || langMatches(lang(?label), "*"))
}
"""
labels = g.query(query, initNs={"rdf": RDF, "rdfs": RDFS, "owl": OWL})

# Group the labels by item using a dictionary
#teste = "Sou o simão"
#lang = TextBlob(teste)
#print(lang.detect_language())

label_dict = {}
for label in labels:
    item_uri = label[0]
    labellang = label[1].language
    if str(labellang) == 'None':
        labellang = lang
    if item_uri not in label_dict:
        label_dict[item_uri] = {}
    if labellang not in label_dict[item_uri]:
        label_dict[item_uri][labellang] = []
    label_dict[item_uri][labellang].append(label[1])

# Print out the labels by item
for item_uri, labels_by_lang in label_dict.items():
    print(f"Item {item_uri}:")
    for lang, labels in labels_by_lang.items():
        print(f"  {lang}:")
        for label in labels:
            print(f"    {label}")


#Em algumas ontologias, a label não vem associada com nenhuma lingua, ficando no dicionario, "None" como a sua lingua
#Soluções : 
#   - assumindo que isto só acontece em ontologias monolingues, pedir ao utilizador a língua em que a ontologia está
#   - implementar alguma função que dada uma str reconheça a lingua em que a mesma está, problema:  
#           - apos algumas tentativas, cheguei a conclusão que os algoritmos que existem de NLP são muito pouco acertivos quando aplicados
#       a pequenas strings como por exemplo uma palavra apenas