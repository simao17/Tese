from flask import Flask, render_template, request, jsonify, send_file
from rdflib import Graph
from translator import translator
from ranking import ranker
from translation_choice import choicer
from output_generator import generator
import main
import codecs
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    xml_file = request.files['xml_file']
    original_lang = request.form['original_lang']
    target_lang = request.form['target_lang']

    g = Graph()

    g.parse(data=xml_file.read(), format='xml') 

    result_xml = main.process(g, original_lang, target_lang, xml_file)

    result_file_path = 'result.xml'
    with codecs.open(result_file_path, 'w', encoding='utf-8') as file:
        file.write(result_xml)

    return send_file(result_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)