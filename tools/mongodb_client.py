""" MongoDB Client """


import os
import threading

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from PyQt5.QtCore import QObject, pyqtSignal

from tools.common import MongoDBStatus
from tools.utils import load_json, save_json

CONFIG_PATH = os.environ['CONFIG_PATH']


class MongoDBClient(QObject):
    """ Mongo Database Client """
    finish_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.config = load_json(CONFIG_PATH)
        self.client = MongoClient(
            self.config.mongodb_endpoint,
            timeoutMS=self.config.mongodb_timeout,
            socketTimeoutMS=self.config.mongodb_timeout,
            connectTimeoutMS=self.config.mongodb_timeout
        )
        database = self.client["invoice_app"]
        self.invoice_col = database["invoices"]
        self.customer_col = database["customer"]
        self.offline_mode = True

        os.makedirs(self.config.backup_folder, exist_ok=True)

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

    def get_id_from_collection(self, data) -> str:
        """ Get id of specific collection """
        collection = self.invoice_col if isinstance(data, list) else self.customer_col
        if not self.offline_mode:
            doc = collection.find_one(data)
            if doc:
                return str(doc["_id"])

    def add_document(self, data_id: str, data) -> bool|str:
        """ Insert one document to specific collection """
        data_dict = {'_id': data_id, 'data': data}
        collection = self.invoice_col if isinstance(data, list) else self.customer_col

        if not self.offline_mode:
            collection.insert_one(data_dict)
            return True
        else:
            save_path = os.path.join(self.config.backup_folder, f"{data_id}.json")
            save_json(data_dict, save_path)
            return save_path

    def delete_document(self, data) -> None:
        """ Delete one document out of collection """
        collection = self.invoice_col if isinstance(data, list) else self.customer_col
        if not self.offline_mode:
            collection.delete_one(data)

    def modify_document(self, data_id: str, new_data, collection) -> None:
        """ Modify invoice infomation """
        if not self.offline_mode:
            collection.update_one(
                {"_id": data_id},
                {'$set': new_data}
            )

    def query_invoice_name(self):
        """ Query invoice by name """
        if not self.offline_mode:
            self.invoice_col.find({}, {"name": 1, "_id": 0 })

    def get_customer_info(self):
        """ Get all customer information """
        if not self.offline_mode:
            return self.customer_col.find()
        else:
            return []

if __name__=="__main__":
    db = MongoDBClient()
    db.check_connection()
