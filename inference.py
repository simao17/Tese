import re

def inference(xml_file1, xml_file2, lang_1A, lang_2A, lang_1B, lang_2B):
    result_ontology = xml_file1[:]
    line_number = 0
    if lang_1A == lang_1B:
        common_lang = lang_1A
    elif lang_1A == lang_2B:
        common_lang = lang_1A
    elif lang_2A == lang_1B:
        common_lang = lang_2A
    elif lang_2A == lang_2B:
        common_lang == lang_2A
    else:
        print("Can't triangulate with the selected languages. One of the languages must match in both ontologies.")
        
    skip_next_line = False

    for line in xml_file1:
        line_number += 1
        if skip_next_line:
            skip_next_line = False
            continue

        if "<rdfs:label" in line:
            id_end = 10
            id = "rdfs:label"
            content_startA1 = line.find(">", id_end) + 1
            content_endA1 = line.find("</rdfs:label>")
            contentA1 = line[content_startA1:content_endA1].strip() or None

            lineB1 = xml_file2[line_number-1]
            lang_matchB1 = re.search(r'xml:lang="([^"]*)"', lineB1)
            langB1 = lang_matchB1.group(1) if lang_matchB1 else None
            content_startB1 = lineB1.find(">", id_end) + 1
            content_endB1 = lineB1.find("</rdfs:label>")
            contentB1 = lineB1[content_startB1:content_endB1].strip() or None

            lineB2 = xml_file2[line_number]
            lang_matchB2 = re.search(r'xml:lang="([^"]*)"', lineB2)
            langB2 = lang_matchB2.group(1) if lang_matchB2 else None
            content_startB2 = lineB2.find(">", id_end) + 1
            content_endB2 = lineB2.find("</rdfs:label>")
            contentB2 = lineB2[content_startB2:content_endB2].strip() or None

            if contentA1 == contentB1:
                skip_next_line = True
                if langB2 == None:
                    result_ontology[line_number-1] = "<"+ id + ">" + contentB2 + "</" + id + ">\n"
                else:
                    result_ontology[line_number-1]= "<"+ id + " xml:lang=\"" + langB2 + "\">" + contentB2 + "</" + id + ">\n"

            elif contentA1 == contentB2:
                skip_next_line = True
                if langB1 == None:
                    result_ontology[line_number-1] = "<"+ id + ">" + contentB1 + "</" + id + ">\n"
                else:
                    result_ontology[line_number-1]= "<"+ id + " xml:lang=\"" + langB1 + "\">" + contentB1 + "</" + id + ">\n"

            else:
                lineA2 = xml_file1[line_number]
                content_startA2 = lineA2.find(">", id_end) + 1
                content_endA2 = lineA2.find("</rdfs:label>")
                contentA2 = lineA2[content_startA2:content_endA2].strip() or None

                if contentA2 == contentB1:
                    skip_next_line = True
                    if langB2 == None:
                        result_ontology[line_number-1] = "<"+ id + ">" + contentB2 + "</" + id + ">\n"
                    else:
                        result_ontology[line_number-1]= "<"+ id + " xml:lang=\"" + langB2 + "\">" + contentB2 + "</" + id + ">\n"

                elif contentA2 == contentB2:
                    skip_next_line = True
                    if langB1 == None:
                        result_ontology[line_number-1] = "<"+ id + ">" + contentB1 + "</" + id + ">\n"
                    else:
                        result_ontology[line_number-1]= "<"+ id + " xml:lang=\"" + langB1 + "\">" + contentB1 + "</" + id + ">\n"

                else:
                    print("Something went wrong")    

        elif "<rdfs:comment" in line:
            id_end = 12
            id = "rdfs:comment"
            content_startA1 = line.find(">", id_end) + 1
            content_endA1 = line.find("</rdfs:comment>")
            contentA1 = line[content_startA1:content_endA1].strip() or None

            lineB1 = xml_file2[line_number-1]
            lang_matchB1 = re.search(r'xml:lang="([^"]*)"', lineB1)
            langB1 = lang_matchB1.group(1) if lang_matchB1 else None
            content_startB1 = lineB1.find(">", id_end) + 1
            content_endB1 = lineB1.find("</rdfs:comment>")
            contentB1 = lineB1[content_startB1:content_endB1].strip() or None

            lineB2 = xml_file2[line_number]
            lang_matchB2 = re.search(r'xml:lang="([^"]*)"', lineB2)
            langB2 = lang_matchB2.group(1) if lang_matchB2 else None
            content_startB2 = lineB2.find(">", id_end) + 1
            content_endB2 = lineB2.find("</rdfs:comment>")
            contentB2 = lineB2[content_startB2:content_endB2].strip() or None

            if contentA1 == contentB1:
                skip_next_line = True
                if langB2 == None:
                    result_ontology[line_number-1] = "<"+ id + ">" + contentB2 + "</" + id + ">\n"
                else:
                    result_ontology[line_number-1]= "<"+ id + " xml:lang=\"" + langB2 + "\">" + contentB2 + "</" + id + ">\n"

            elif contentA1 == contentB2:
                skip_next_line = True
                if langB1 == None:
                    result_ontology[line_number-1] = "<"+ id + ">" + contentB1 + "</" + id + ">\n"
                else:
                    result_ontology[line_number-1]= "<"+ id + " xml:lang=\"" + langB1 + "\">" + contentB1 + "</" + id + ">\n"

            else:
                lineA2 = xml_file1[line_number]
                content_startA2 = lineA2.find(">", id_end) + 1
                content_endA2 = lineA2.find("</rdfs:comment>")
                contentA2 = lineA2[content_startA2:content_endA2].strip() or None

                if contentA2 == contentB1:
                    skip_next_line = True
                    if langB2 == None:
                        result_ontology[line_number-1] = "<"+ id + ">" + contentB2 + "</" + id + ">\n"
                    else:
                        result_ontology[line_number-1]= "<"+ id + " xml:lang=\"" + langB2 + "\">" + contentB2 + "</" + id + ">\n"

                elif contentA2 == contentB2:
                    skip_next_line = True
                    if langB1 == None:
                        result_ontology[line_number-1] = "<"+ id + ">" + contentB1 + "</" + id + ">\n"
                    else:
                        result_ontology[line_number-1]= "<"+ id + " xml:lang=\"" + langB1 + "\">" + contentB1 + "</" + id + ">\n"

                else:
                    print("Something went wrong")

        elif "xml:lang=" in line:
            id_start = line.find("<") + 1
            id_end = line.find(" ", id_start)
            id = line[id_start:id_end]

            content_startA1 = line.find(">", id_end) + 1
            content_endA1 = line.find("</")
            contentA1 = line[content_startA1:content_endA1].strip() or None

            lineB1 = xml_file2[line_number-1]
            lang_matchB1 = re.search(r'xml:lang="([^"]*)"', lineB1)
            langB1 = lang_matchB1.group(1) if lang_matchB1 else None
            content_startB1 = lineB1.find(">", id_end) + 1
            content_endB1 = lineB1.find("</")
            contentB1 = lineB1[content_startB1:content_endB1].strip() or None

            lineB2 = xml_file2[line_number]
            lang_matchB2 = re.search(r'xml:lang="([^"]*)"', lineB2)
            langB2 = lang_matchB2.group(1) if lang_matchB2 else None
            content_startB2 = lineB2.find(">", id_end) + 1
            content_endB2 = lineB2.find("</")
            contentB2 = lineB2[content_startB2:content_endB2].strip() or None

            if contentA1 == contentB1:
                skip_next_line = True
                if langB2 == None:
                    result_ontology[line_number-1] = "<"+ id + ">" + contentB2 + "</" + id + ">\n"
                else:
                    result_ontology[line_number-1]= "<"+ id + " xml:lang=\"" + langB2 + "\">" + contentB2 + "</" + id + ">\n"

            elif contentA1 == contentB2:
                skip_next_line = True
                if langB1 == None:
                    result_ontology[line_number-1] = "<"+ id + ">" + contentB1 + "</" + id + ">\n"
                else:
                    result_ontology[line_number-1]= "<"+ id + " xml:lang=\"" + langB1 + "\">" + contentB1 + "</" + id + ">\n"

            else:
                lineA2 = xml_file1[line_number]
                content_startA2 = lineA2.find(">", id_end) + 1
                content_endA2 = lineA2.find("</")
                contentA2 = lineA2[content_startA2:content_endA2].strip() or None

                if contentA2 == contentB1:
                    skip_next_line = True
                    if langB2 == None:
                        result_ontology[line_number-1] = "<"+ id + ">" + contentB2 + "</" + id + ">\n"
                    else:
                        result_ontology[line_number-1]= "<"+ id + " xml:lang=\"" + langB2 + "\">" + contentB2 + "</" + id + ">\n"

                elif contentA2 == contentB2:
                    skip_next_line = True
                    if langB1 == None:
                        result_ontology[line_number-1] = "<"+ id + ">" + contentB1 + "</" + id + ">\n"
                    else:
                        result_ontology[line_number-1]= "<"+ id + " xml:lang=\"" + langB1 + "\">" + contentB1 + "</" + id + ">\n"

                else:
                    print("Something went wrong")

    modified_xml = ''.join(result_ontology)
    return modified_xml