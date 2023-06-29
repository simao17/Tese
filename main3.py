from translator2 import translator
from ranking import ranker
from translation_choice import choicer
from output_generator2 import generator

original_lang = "en"
target_lang = "pt"

translated_data = translator("./teste2.xml", original_lang, target_lang)
translated_data_ranked = ranker(translated_data)
translated_data_chose = choicer(translated_data_ranked)
final_ontology = generator(translated_data_chose, "./teste2.xml", target_lang)

print("SUCCESS!")