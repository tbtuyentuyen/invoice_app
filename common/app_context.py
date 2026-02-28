""" Application context module """

import os
import shutil

from pydotdict import DotDict

from tools.utils import load_json, save_json
from tools.mongodb_client import MongoDBClient

CONFIG_DIR = os.environ['CONFIG_DIR']
CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.json')
INVOICE_APP_PATH = os.environ['INVOICE_APP_PATH']
BASE_DATA_PATH = os.path.join(INVOICE_APP_PATH, 'data')

class AppContext():
    """ Application context class """
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.config = self.load_config()

    def load_config(self) -> DotDict:
        """ Load configuration from file """
        return load_json(CONFIG_PATH)

    def save_config(self) -> None:
        """ Save configuration to file """
        save_json(self.config, CONFIG_PATH)

    @staticmethod
    def generate_user_data():
        """ Generate config folder if not exist """
        assert os.path.isdir(BASE_DATA_PATH), f"Source path does not exist: {BASE_DATA_PATH}"

        if not os.path.isdir(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)

        for entry in os.listdir(BASE_DATA_PATH):
            src_path = os.path.join(BASE_DATA_PATH, entry)
            dest_path = os.path.join(CONFIG_DIR, entry)

            # Folder: copy entire folder if it does not exist in destination
            if os.path.isdir(src_path):
                if not os.path.exists(dest_path):
                    shutil.copytree(src_path, dest_path)
            else:
                # File: copy file if it does not exist in destination
                if not os.path.exists(dest_path):
                    shutil.copy2(src_path, dest_path)

                else:
                    # Content: merge content if it's a json file
                    if entry.endswith('.json'):
                        src_data = load_json(src_path)
                        dest_data = load_json(dest_path)

                        # If keys are different, merge and save
                        if src_data.keys() != dest_data.keys():
                            merged_data = {**src_data, **dest_data}
                            save_json(merged_data, dest_path)
