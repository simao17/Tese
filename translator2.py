import re
import deepl
from deep_translator import LingueeTranslator

def translator(xml_file, orgn_lang, target_lang):
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

    
    xml_file_path = "./teste4.xml"

    with open(xml_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    line_number = 0
    line_info = []

    for line in lines:
        line_number += 1

        if "<rdfs:label" in line:
            id_start = line.find("<") + 1
            id_end = 10
            id = "rdfs:label"

            lang_match = re.search(r'xml:lang="([^"]*)"', line)
            lang = lang_match.group(1) if lang_match else orgn_lang

            content_start = line.find(">", id_end) + 1
            content_end = line.find("</rdfs:label>")
            content = line[content_start:content_end].strip() or None

            line_info.append((line_number, id, lang, content))

        elif "<rdfs:comment" in line:
            id_start = line.find("<") + 1
            id_end = 12
            id = "rdfs:comment"

            lang_match = re.search(r'xml:lang="([^"]*)"', line)
            lang = lang_match.group(1) if lang_match else None

            content_start = line.find(">", id_end) + 1
            content_end = line.find("</rdfs:comment>")
            content = line[content_start:content_end].strip() or None

            line_info.append((line_number, id, lang, content))

        elif "xml:lang=" in line:
            id_start = line.find("<") + 1
            id_end = line.find(" ", id_start)
            id = line[id_start:id_end]

            lang_match = re.search(r'xml:lang="([^"]*)"', line)
            lang = lang_match.group(1) if lang_match else None

            content_start = line.find(">", id_end) + 1
            content_end = line.find("</")
            content = line[content_start:content_end].strip() or None

            line_info.append((line_number, id, lang, content))

    translated_lines=[]
    last_line_number, last_id, last_lang, last_content = (-5, "","","")
    # Iterate over the line_info list
    for line in line_info:

        line_number, id, lang, content = line

        if id == "rdfs:comment":
            if (content is not None and len(content)!=0 and content!='None'):
                translated_comment = translator.translate_text(content, source_lang=lang, target_lang=deepl_langs[target_lang]).text
                translated_lines.append((line_number, id, lang, content, translated_comment))
            else:
                translated_lines.append((line_number, id, lang, content, 'None'))

        elif id == "rdfs:label":
            #if it's not the same label but in a different language, then translate it
            if not (last_line_number+1==line_number and last_id == id and last_lang != lang):
                if len(re.findall(r'\w+', content)) == 1:
                        #if the label is only one word, translate with Linguee because it gives several possible outputs and synonims
                        #try except block, because for some words p.e. "Mary", Linguee does not have translations
                        try:
                            translated_label = LingueeTranslator(source=available_langs[lang], target=available_langs[target_lang]).translate(content, return_all=True)
                        except:
                            translated_label = translator.translate_text(content, source_lang=lang, target_lang=deepl_langs[target_lang]).text
                else:
                    #else, use deepl to translate, as it works better for sentences, and already should translate correctly depending on the context
                    translated_label = translator.translate_text(content, source_lang=lang, target_lang=deepl_langs[target_lang]).text

                translated_lines.append((line_number, id, lang, content, translated_label))
        
        else:
            if not (last_line_number+1==line_number and last_id == id and last_lang != lang):
                translated_line = translator.translate_text(content, source_lang=lang, target_lang=deepl_langs[target_lang]).text
                translated_lines.append((line_number, id, lang, content, translated_line))
        
        last_line_number, last_id, last_lang, last_content = line

    for line in translated_lines:
        a, b, c, d, e = line
        print(f"Line number: {a}, ID: {b}, Lang: {c}, Content: {d}, Translated Content: {e}")

    return(translated_lines)