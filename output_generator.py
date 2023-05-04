from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
def generator(labels, comments, g):
    #g = Graph()
    #g.parse(data=owl_file.read(), format='xml')

    for item_uri, data in labels.items():
        uri = URIRef(item_uri)
        for label_lang, label in data.items():
            g.add((uri, RDFS.label, Literal(label, lang=label_lang)))

    for item_uri, data in comments.items():
        uri = URIRef(item_uri)
        for comment_lang, comment in data.items():
            g.add((uri, RDFS.comment, Literal(comment, lang=comment_lang)))

    g.serialize("./modified_teste2.owl", format="xml")