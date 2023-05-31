from translator import translator
from ranking import ranker
from translation_choice import choicer
from teste import add_labels_to_ontology
from output_generator import generator

def process(graph, original_lang, target_lang, xml_file):
    labels, comments= translator(graph, original_lang, target_lang)
    labels2, comments2 = ranker(labels, comments)
    labels3, comments3 = choicer(labels2,comments2)
    final_ontology = add_labels_to_ontology(labels3, xml_file)
    #final_ontology = generator(labels3, comments3, xml_file)
    return final_ontology
