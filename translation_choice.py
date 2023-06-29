def choicer(translated_lines):
    updated_lines=[]
    for line in translated_lines:
        line_number, id, lang, content, translated = line
        if isinstance(translated, list):
            translated = translated[0]  # for now we are not taking into account the context of the ontology,
        updated_lines.append((line_number, id, lang, content, translated))                                                 # picking the first translation as the best one
    return(updated_lines)

#falta depois colocar a opção de através do logfile, introduzindo o item_uri, editar a label para o que o utilizador quiser