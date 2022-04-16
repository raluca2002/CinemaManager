def clear_file(filename) -> None:
    """
    deschide un fisier si il inchide automat la funalizarea lui "with"
    :param filename: numele fisierului
    :return:
    """
    with open(filename, "w"):
        pass
