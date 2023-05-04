from flask import Flask, render_template, request, jsonify
from rdflib import Graph
import main

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

    result = main.process(g, original_lang, target_lang)
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)