import xml.etree.ElementTree as ET

def add_labels_to_ontology(labels_dict, ontology_file):
    # Parse the ontology from the uploaded file
    tree = ET.parse(ontology_file)
    root = tree.getroot()

    # Iterate over the labels dictionary and add labels to the ontology
    for item_uri, label_info in labels_dict.items():
        for description in root.iter('{http://www.w3.org/2002/07/owl#}Description'):
            about = description.attrib.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about')
            if about == item_uri:
                # Create a new label element and append it to the Description element
                label = ET.SubElement(description, '{http://www.w3.org/2000/01/rdf-schema#}label')
                label.text = label_info["label_lang"]
                label.set('{http://www.w3.org/XML/1998/namespace}lang', label_info["language"])

    # Return the modified ontology XML content
    modified_ontology = ET.tostring(root, encoding='utf-8').decode('utf-8')
    return modified_ontology