from flask import Flask, render_template, request, jsonify, send_file
import main
import codecs
import tempfile
import io
import logging
import sys

app = Flask(__name__)

# Adjust Flask's logging level to capture only necessary logs
app.logger.setLevel(logging.INFO)
app.logger.handlers = [logging.StreamHandler(sys.stdout)]

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True)