from translator import translator
from ranking import ranker
from translation_choice import choicer
from output_generator import generator


labels, comments, ontology_file_path = translator()


labels2, comments2 = ranker(labels, comments)
labels3, comments3 = choicer(labels2,comments2)
final_ontology = generator(labels3, comments3, ontology_file_path)
