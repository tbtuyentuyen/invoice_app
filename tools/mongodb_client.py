""" MongoDB Client """


import os
import threading

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from PyQt5.QtCore import QObject, pyqtSignal

from tools.common import MongoDBStatus, DBCollection
from tools.utils import load_json, save_json, expand_env_vars_in_path

CONFIG_DIR = os.environ['CONFIG_DIR']

class MongoDBClient(QObject):
    """ Mongo Database Client """
    finish_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.config = load_json(os.path.join(CONFIG_DIR, 'config.json'))
        self.client = MongoClient(
            self.config.mongodb_endpoint,
            timeoutMS=self.config.mongodb_timeout,
            socketTimeoutMS=self.config.mongodb_timeout,
            connectTimeoutMS=self.config.mongodb_timeout
        )
        database = self.client["invoice_app"]
        self.collections = {
            DBCollection.INVOICE: database[DBCollection.INVOICE.name.lower()],
            DBCollection.CUSTOMER: database[DBCollection.CUSTOMER.name.lower()],
            DBCollection.PRODUCT: database[DBCollection.PRODUCT.name.lower()]
        }
        self.offline_mode = True

        os.makedirs(expand_env_vars_in_path(self.config.backup_folder), exist_ok=True)

    def start(self):
        """ Start MongoDB Client """
        mongodb_thread = threading.Thread(target=self.check_connection, name="MongoDBThread", daemon=True)
        mongodb_thread.start()

    def check_connection(self):
        """ Check connect to MongoDB """
        try:
            self.client.server_info()
            self.offline_mode = False
            self.finish_signal.emit(MongoDBStatus.CONNECTED.value)
        except ServerSelectionTimeoutError:
            self.offline_mode = True
            self.finish_signal.emit(MongoDBStatus.DISCONNECTED.value)
        except Exception:  # pylint: disable=broad-exception-caught
            self.offline_mode = True
            self.finish_signal.emit(MongoDBStatus.UNKNOWN.value)

    def disconnect_client(self):
        """ Disconnect to MongoDB"""
        if not self.offline_mode:
            self.client.close()

    def add_document(
            self,
            data: dict,
            collection_type: DBCollection
        ) -> bool|str:
        """ Insert one document to specific collection """
        collection = self.collections[collection_type]
        data_id = data.get("_id", None)
        if not data_id:
            return False

        if not self.offline_mode:
            if data_id in collection.distinct("_id"):
                collection.replace_one({'_id': data_id}, data)
            else:
                collection.insert_one(data)
            return True
        else:
            save_path = os.path.join(expand_env_vars_in_path(self.config.backup_folder), f"{data_id}.json")
            save_json(data, save_path)
            return save_path

    def get_customer_info(self):
        """ Get all customer information """
        if not self.offline_mode:
            return self.collections[DBCollection.CUSTOMER].find()
        else:
            return []

if __name__=="__main__":
    db = MongoDBClient()
    db.check_connection()
