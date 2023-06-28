from rdflib import Graph, Namespace
from googletrans import Translator
import deepl
from deep_translator import LingueeTranslator
import re

def translator(g, lang, target_lang):
    auth_key = '8b2ab6f0-50c1-4212-8be6-ef0f49f583e4:fx'
    translator = deepl.Translator(auth_key)

    available_langs = {
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
        "sv": "swedish",
        "lv": "latvian",
        "et": "estonian",
        "ja": "japanese"
    }

    deepl_langs = {
        "pt": "pt-pt",
        "en": "en-gb",
        "de": "de",
        "bg": "bg",
        "pl": "pl",
        "hu": "hu",
        "ro": "ro",
        "ru": "ru",
        "nl": "nl",
        "sk": "sk",
        "el": "el",
        "sl": "sl",
        "da": "da",
        "it": "it",
        "es": "es",
        "fi": "fi",
        "zh": "zh",
        "sv": "sv",
        "lv": "lv",
        "et": "et",
        "cs": "cs",
        "fr": "fr",
        "ja": "ja"
    }
    """
    langs_pairs = [f"{key} - {value}" for key, value in available_langs.items()]

    prompt = "From the following list, select the language you want to add to the ontology:\n" + "\n".join(langs_pairs) + "\n\nInsert language(the short way): "
    # Prompt the user to enter the path to the OWL ontology file    
    lang = input("If applicable enter the language of the ontology in ISO 639-1 format (https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes): ")
    target_lang = input(prompt)

    while target_lang not in available_langs.keys():
        target_lang = input("Something went wrong. Insert the language again and please be careful to put it in the short format: ")
    """

    # Load the OWL ontology into an rdflib Graph object
    #g = Graph()
    #g.parse(data=owl_file.read(), format='xml')

    # Define the RDF namespaces used in the OWL ontology
    RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    OWL = Namespace("http://www.w3.org/2002/07/owl#")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    xml = Namespace("http://www.w3.org/XML/1998/namespace")

    # Query the rdflib Graph for all items and their associated labels and comments
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

    """
    with open("result.txt", "w") as file:
        for row in extracted:
            item_uri = row['item']
            label_content = row['label']
            comment_content = row['comment']
            line_content = row['lineContent']
            line_uri = row['lineURI']
            line_lang = row['lineLang']

            if line_content is not None:
                line_content = line_content.split(' ', 1)[1]    

            # Write the information to the file
            file.write("Item URI: {}\n".format(item_uri))
            file.write("Label Content: {}\n".format(label_content))
            file.write("Comment Content: {}\n".format(comment_content))
            file.write("Line Content: {}\n".format(line_content))
            file.write("Line URI: {}\n".format(line_uri))
            file.write("Line Language: {}\n".format(line_lang))
            file.write("------------------------\n")
    """
    label_dict = {}
    for result in extracted:
        item_uri = result['item']
        label_lang = result['label'].language
        #line_content = result['lineContent']
        #line_lang = result['lineLang']
        if str(label_lang) == 'None':                        
            label_lang = lang                               # Set label_lang to lang if it does'nt have any language associated
        if item_uri not in label_dict:
            label_dict[item_uri] = {}
            label_dict[item_uri]['comments'] = set()
            #label_dict[item_uri]['lines'] = {}
        if result[2] is not None:                           # result[2] corresponds to the comment extracted
            comment_lang = result[2].language or lang       # Set comment_lang to lang if it does'nt have any language associated
            label_dict[item_uri]['comments'].add((result[2], comment_lang))         # Add comment to the set
        #if line_content is not None:
            #label_dict[item_uri]['lines'][line_content] = line_lang
        label_dict[item_uri][label_lang] = result[1]        # Assign label to corresponding language

    

    for item_uri, results in label_dict.items():
        print(f"Item {item_uri}:")
        if 'comments' in results:
            for comment, comment_lang in results['comments']:
                print(f"  Comment ({comment_lang}): {comment}")
        for labellang, label in results.items():
            if labellang != 'comments':
                print(f"  {labellang}:")
                print(f"    {label}")

    translations_label_dict={}
    translations_comments_dict={}
    translations_lines_dict = {}
    #Access every comment and every label to translate them
    for item_uri, item_data in label_dict.items():
        translations_label_dict[item_uri]={}
        translations_comments_dict[item_uri]={}
        translations_lines_dict[item_uri] = {}
        

        #Translate Comment
        if item_data['comments']:
            # Get first comment
            comment, comment_lang = next(iter(item_data['comments']))   
            #translate comment  
            if(len(comment)!=0 and comment!='None'):
                translated_comment = translator.translate_text(comment, source_lang=comment_lang, target_lang=deepl_langs[target_lang]).text
            # Add translated comment to dictionary
            translations_comments_dict[item_uri][target_lang] = translated_comment

        #Translate label
        for lang, label in item_data.items():
            if lang != 'comments':          # Skip comments
                #Translate label
                if len(re.findall(r'\w+', label)) == 1:
                    #if the label is only one word, translate with Linguee because it gives several possible outputs and synonims
                    #try except block, because for some words p.e. "Mary", Linguee does not have translations
                    try:
                        translated_label = LingueeTranslator(source=available_langs[lang], target=available_langs[target_lang]).translate(label, return_all=True)
                    except:
                        translated_label = translator.translate_text(label, source_lang=lang, target_lang=deepl_langs[target_lang]).text
                else:
                    #else, use deepl to translate, as it works better for sentences, and already should translate correctly depending on the context
                    translated_label = translator.translate_text(label, source_lang=lang, target_lang=deepl_langs[target_lang]).text
                translations_label_dict[item_uri][target_lang] = translated_label
                break
    return(translations_label_dict, translations_comments_dict)