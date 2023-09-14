import logging
import datetime
import os
import deepl

def clean_log_file(log_file):
    if os.path.exists(log_file):
        os.remove(log_file)

def ranker(translated_lines, ontology_context, target_lang):
    logger = logging.getLogger("translation")
    logger.setLevel(logging.INFO)

    auth_key = '8b2ab6f0-50c1-4212-8be6-ef0f49f583e4:fx'
    translator = deepl.Translator(auth_key)

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

    # Add a FileHandler if not already present
    if not logger.handlers:
        logger.addHandler(logging.FileHandler("program.log"))

    # Set the log file name
    logger.handlers[0].baseFilename = "program.log"

    # Clean the log file before each execution
    open("program.log", 'w', encoding="utf-8").close()

    updated_lines = []
    for line in translated_lines:
        line_number, id, lang, content, translated = line
        print(translated)
        if isinstance(translated, list):
            new_content = ontology_context + ', ' + content.lower()
            translation = translator.translate_text(new_content, source_lang=lang, target_lang=deepl_langs[target_lang]).text
            #print(translation)
            best_translation = translation.split(", ")[1]
            if best_translation in translated: 
                logger.info(f"Multiple translations found for line {line_number} for {content}. Choosing '{best_translation}' from options {translated}.")
                translated = best_translation
            else:
                logger.info(f"Multiple translations found for line {line_number} for {content}. Choosing '{translated[0]}' from options {translated}.")
                translated = translated[0]  # Choosing the first translation as the best one

        updated_lines.append((line_number, id, lang, content, translated))
    return updated_lines