from flask import Flask, render_template, request, jsonify, send_file
import main
import codecs
import io
import logging
import sys
from datetime import datetime

app = Flask(__name__)

# Adjust Flask's logging level to capture only necessary logs
app.logger.setLevel(logging.INFO)
app.logger.handlers = [logging.StreamHandler(sys.stdout)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inference')
def result():
    return render_template('inference.html')

@app.route('/triangulation', methods=['POST'])
def triangulation():
    xml_file1 = request.files['xml_file1']
    xml_file2 = request.files['xml_file2']
    lang1A = "smthing"#request.form['lang_1a']
    lang2A = "smthing"#request.form['lang_2a']
    lang1B = ""#request.form['lang_1b']
    lang2B = ""#request.form['lang_2b']

    # Open the file and read the lines
    file_content1 = io.StringIO(xml_file1.stream.read().decode('utf-8'))
    lines1 = file_content1.readlines()

    file_content2 = io.StringIO(xml_file2.stream.read().decode('utf-8'))
    lines2 = file_content2.readlines()

    result_ontology = main.triangulation(lines1, lines2, lang1A, lang1B, lang2A, lang2B)

    result_file_path = 'result.xml'
    with codecs.open(result_file_path, 'w', encoding='utf-8') as file:
        file.write(result_ontology)

    return send_file(result_file_path, as_attachment=True)

@app.route('/process', methods=['POST'])
def process():
    xml_file = request.files['xml_file']
    original_lang = request.form['original_lang']
    target_lang = request.form['target_lang']
    ontology_context = request.form['ontology_context']

    # Open the file and read the lines
    file_content = io.StringIO(xml_file.stream.read().decode('utf-8'))
    lines = file_content.readlines()

    result_xml = main.process(lines, original_lang, target_lang, ontology_context)

    result_file_path = 'result.xml'
    with codecs.open(result_file_path, 'w', encoding='utf-8') as file:
        file.write(result_xml)

    return send_file(result_file_path, as_attachment=True)

@app.route('/download_logfile', methods=['GET'])
def download_logfile():
    program_log_path = './program.log'

    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    download_filename = f'program_{current_datetime}.log'

    return send_file(
        program_log_path,
        as_attachment=True,
        download_name=download_filename,
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(debug=True)