from translator2 import translator
from ranking import ranker
from translation_choice import choicer
from output_generator2 import generator
from inference import inference

def process(xml_file, original_lang, target_lang, ontology_context):
    translated_data = translator(xml_file, original_lang, target_lang)
    translated_data_ranked = ranker(translated_data, ontology_context, target_lang)
    #translated_data_chose = choicer(translated_data_ranked)
    final_ontology = generator(translated_data_ranked, xml_file, target_lang)

    return final_ontology

def triangulation(xml_file1, xml_file2, lang_1A, lang_2A, lang_1B, lang_2B):
    result_ontology = inference(xml_file1, xml_file2, lang_1A, lang_2A, lang_1B, lang_2B)
    return result_ontology