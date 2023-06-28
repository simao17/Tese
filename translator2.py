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

    with open(xml_file_path, "r", encoding="utf-8") as file:
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
        
    # Iterate over the line_info list
    for line in line_info:
        line_number, id, lang, content = line
        print(f"Line {line_number}: ID: {id}, Language: {lang}, Content: {content}")