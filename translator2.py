import re

xml_file_path = "./teste4.xml"

with open(xml_file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

line_number = 0

for line in lines:
    line_number += 1

    if "<rdfs:label" in line:
        uri_start = line.find("<") + 1
        uri_end = 10
        uri = "rdfs:label"

        lang_match = re.search(r'xml:lang="([^"]*)"', line)
        lang = lang_match.group(1) if lang_match else None

        content_start = line.find(">", uri_end) + 1
        content_end = line.find("</rdfs:label>")
        content = line[content_start:content_end].strip() or None

        print(f"Line {line_number}: URI: {uri}, Language: {lang}, Content: {content}")

    elif "<rdfs:comment" in line:
        uri_start = line.find("<") + 1
        uri_end = 12
        uri = "rdfs:comment"

        lang_match = re.search(r'xml:lang="([^"]*)"', line)
        lang = lang_match.group(1) if lang_match else None

        content_start = line.find(">", uri_end) + 1
        content_end = line.find("</rdfs:comment>")
        content = line[content_start:content_end].strip() or None

        print(f"Line {line_number}: URI: {uri}, Language: {lang}, Content: {content}")

    elif "xml:lang=" in line:
        uri_start = line.find("<") + 1
        uri_end = line.find(" ", uri_start)
        uri = line[uri_start:uri_end]

        lang_match = re.search(r'xml:lang="([^"]*)"', line)
        lang = lang_match.group(1) if lang_match else None

        content_start = line.find(">", uri_end) + 1
        content_end = line.find("</")
        content = line[content_start:content_end].strip() or None

        print(f"Line {line_number}: URI: {uri}, Language: {lang}, Content: {content}")
