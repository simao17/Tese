from translator import translator
from ranking import ranker
from translation_choice import choicer
from output_generator import generator

def process(owl_file, original_lang, target_lang):
    labels, comments= translator(owl_file, original_lang, target_lang)
    labels2, comments2 = ranker(labels, comments)
    labels3, comments3 = choicer(labels2,comments2)
    final_ontology = generator(labels3, comments3, owl_file)
    return final_ontology
