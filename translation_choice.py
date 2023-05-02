def choicer(labels, comments):
    for item_uri, data in labels.items():
        for label_lang, label in data.items():
            if isinstance(label, list):
                labels[item_uri][label_lang] = label[0]  # for now we are not taking into account the context of the ontology,
                                                         # picking the first translation as the best one
    return(labels, comments)

#falta depois colocar a opção de através do logfile, introduzindo o item_uri, editar a label para o que o utilizador quiser