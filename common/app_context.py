""" Application context module """

import os

from tools.utils import load_json
from tools.mongodb_client import MongoDBClient

CONFIG_DIR = os.environ['CONFIG_DIR']

class AppContext(): # pylint:disable=R0903
    """ Application context class """
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.config = load_json(os.path.join(CONFIG_DIR, 'config.json'))
