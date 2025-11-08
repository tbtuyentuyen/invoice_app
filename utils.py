""" Utilities Module """


import json
from pydotdict import DotDict


def load_json(path: str) -> dict:
    """ Load json data"""
    with open(path, mode='r', encoding='utf-8') as f:
        data = json.load(f)
    return DotDict(data)
