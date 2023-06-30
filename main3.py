from translator2 import translator
from ranking import ranker
from translation_choice import choicer
from output_generator2 import generator

def process(xml_file, original_lang, target_lang):
    translated_data = translator(xml_file, original_lang, target_lang)
    translated_data_ranked = ranker(translated_data)
    translated_data_chose = choicer(translated_data_ranked)
    final_ontology = generator(translated_data_chose, xml_file, target_lang)

    return final_ontology