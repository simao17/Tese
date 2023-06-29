def generator(translated_lines, xml_file, target_lang):
    # Read the XML file into memory
    with open(xml_file, 'r', encoding="utf-8") as file:
        xml_content = file.readlines()

    # Create a copy of the XML content
    modified_content = xml_content[:]
    
    shift = 0
    # Iterate through the list of tuples
    for line in translated_lines:
        line_number, id, lang, content, translated = line
        if translated != "None":
            xml_line = "<"+ id + " xml:lang=\"" + target_lang + "\">" + translated + "</" + id + ">"
            # Get the indentation of the line before the insertion point
            indentation = get_indentation(xml_content[line_number - 1])
            # Add the indentation to the new line
            indented_line = indentation + xml_line
            modified_content.insert(line_number + shift, indented_line + '\n')
            shift += 1

    # Write the modified XML content to the new file
    with open("./resultado.xml", 'w', encoding="utf-8") as file:
        file.writelines(modified_content)

    return True

def get_indentation(line):
    # Calculate the indentation of the line
    indentation = ""

    for char in line:
        if char.isspace():
            indentation += char
        else:
            break

    return indentation