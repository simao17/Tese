from rdflib import Graph, Namespace
from googletrans import Translator
import deepl_api
from deep_translator import LingueeTranslator
import re

available_langs = {
    "mt": "maltese",
    "en": "english",
    "de": "german",
    "bg": "bulgarian",
    "pl": "polish",
    "pt": "portuguese",
    "hu": "hungarian",
    "ro": "romanian",
    "ru": "russian",
    "nl": "dutch",
    "sk": "slovakian",
    "el": "greek",
    "sl": "slovenian",
    "da": "danish",
    "it": "italian",
    "es": "spanish",
    "fi": "finnish",
    "zh": "chinese",
    "fr": "french",
    "cs": "czech",
    "lo": "laotian",
    "sv": "swedish",
    "lv": "latvian",
    "et": "estonian",
    "ja": "japanese"
}

langs_pairs = [f"{key} - {value}" for key, value in available_langs.items()]

prompt = "From the following list, select the language you want to add to the ontology:\n" + "\n".join(langs_pairs) + "\n\nInsert language(the short way): "
# Prompt the user to enter the path to the OWL ontology file    
owl_file_path = input("Enter the path to your OWL ontology file: ")
lang = input("If applicable enter the language of the ontology in ISO 639-1 format (https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes): ")
target_lang = input(prompt)

while target_lang not in available_langs.keys():
    target_lang = input("Something went wrong. Insert the language again and please be careful to put it in the short format: ")

# Load the OWL ontology into an rdflib Graph object
g = Graph()
g.parse(owl_file_path)

# Define the RDF namespaces used in the OWL ontology
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")

# Query the rdflib Graph for all items and their associated labels and comments
#
query = """
SELECT ?item ?label ?comment
WHERE {
  ?item rdfs:label ?label .
  OPTIONAL { ?item rdfs:comment ?comment }
  FILTER(lang(?label) = "" || langMatches(lang(?label), "*"))
  FILTER(!bound(?comment) || lang(?comment) = "" || langMatches(lang(?comment), "*"))
}
"""
extracted = g.query(query, initNs={"rdf": RDF, "rdfs": RDFS, "owl": OWL})

label_dict = {}
for result in extracted:
    item_uri = result[0]
    labellang = result[1].language
    if str(labellang) == 'None':
        labellang = lang
    if item_uri not in label_dict:
        label_dict[item_uri] = {}
        label_dict[item_uri]['comments'] = set()            # Add a set to store comments
    if labellang not in label_dict[item_uri]:
        label_dict[item_uri][labellang] = []
    if result[2] is not None:           # result[2] corresponds to the comment extracted
        comment_lang = result[2].language or lang           # Set comment_lang to lang if it does'nt have any language associated
        label_dict[item_uri]['comments'].add((result[2], comment_lang))         # Add comment to the set
    if result[1] not in label_dict[item_uri][labellang]:
        label_dict[item_uri][labellang].append(result[1])           # Append label to corresponding language

for item_uri, results in label_dict.items():
    print(f"Item {item_uri}:")
    if 'comments' in results:
        for comment, comment_lang in results['comments']:
            print(f"  Comment ({comment_lang}): {comment}")
    for labellang, label_list in results.items():
        if labellang != 'comments':
            label_text = ', '.join(str(lit) for lit in label_list)
            print(f"  {labellang}:")
            print(f"    {label_text}")


#for translation in translations:
#    print(translation.text)

word = 'cuida-te'
translated_word = LingueeTranslator(source='portuguese', target='english').translate(word, return_all=True)
print(translated_word)