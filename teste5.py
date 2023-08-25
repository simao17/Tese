from deep_translator import LingueeTranslator
import deepl

auth_key = '8b2ab6f0-50c1-4212-8be6-ef0f49f583e4:fx'
translator = deepl.Translator(auth_key)

#translated_label = LingueeTranslator(source="portuguese", target="english").translate("musica, bateria", return_all=True)

translated_label = translator.translate_text("jardim, folha", source_lang="pt", target_lang="en-gb").text

print(translated_label)