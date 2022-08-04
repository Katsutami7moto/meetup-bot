import json
from pathlib import Path

DATA_FOLDER = 'data'


def read_json(filename: str):
    """Десериализовать JSON"""
    path_ = Path.cwd() / Path(DATA_FOLDER) / filename
    with open(path_, 'r', encoding='utf8') as file_:
        return json.load(file_)


def write_json(data, filename: str):
    """Сериализовать JSON"""
    path_ = Path.cwd() / Path(DATA_FOLDER) / filename
    with open(path_, 'w', encoding='utf8') as file_:
        json.dump(data, file_, indent=4, ensure_ascii=False)
