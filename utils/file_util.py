import json


def write_json(dictionary, path_file):
    """
    Grava um dict em formato json de arquivo
    Args:
        dictionary: dict a ser gravado
        path_file: caminho do arquivo

    Returns:
        void
    """
    with open(path_file, 'w') as f:
        json.dump(dictionary, f)


def read_json(path_file):
    """
    Le um json apartir de um arquivo e converte para dic
    Args:
        path_file: caminho do arquivo

    Returns:
        dict convertido
    """
    with open(path_file) as f:
        return json.load(f)
