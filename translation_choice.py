import logging
import datetime
import os

def clean_log_file(log_file):
    if os.path.exists(log_file):
        os.remove(log_file)

def choicer(translated_lines):
    logger = logging.getLogger("translation")
    logger.setLevel(logging.INFO)

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
        if isinstance(translated, list):
            logger.info(f"Multiple translations found for line {line_number} for {content}. Choosing '{translated[0]}' from options {translated}.")
            translated = translated[0]  # Choosing the first translation as the best one
        updated_lines.append((line_number, id, lang, content, translated))
    return updated_lines


# Generate a new log file name with a timestamp
#log_file = f"program.log"

# Clean the log file before each execution
#clean_log_file(log_file)

#falta depois colocar a opção de através do logfile, introduzindo o item_uri, editar a label para o que o utilizador quiser