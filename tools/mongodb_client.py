""" MongoDB Client """


import os
import threading

from pymongo import MongoClient
from PyQt5.QtCore import QObject, pyqtSignal

from common.constants import MongoDBStatus, DBCollection
from tools.utils import load_json

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
        self.is_connected = True

    def start(self):
        """ Start MongoDB Client """
        mongodb_thread = threading.Thread(
            target=self.check_connection,
            name="MongoDBThread",
            daemon=True
        )
        mongodb_thread.start()

    def check_connection(self):
        """ Check connect to MongoDB """
        try:
            self.client.server_info()
            self.is_connected = True
            self.finish_signal.emit(MongoDBStatus.CONNECTED.value)
        except Exception:  # pylint: disable=broad-exception-caught
            self.is_connected = False

        return self.is_connected

    def disconnect_client(self):
        """ Disconnect to MongoDB"""
        if self.is_connected:
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

        if not self.is_connected:
            return False

        if data_id in collection.distinct("_id"):
            collection.replace_one({'_id': data_id}, data)
        else:
            collection.insert_one(data)
        return True

    def get_customer_info(self) -> list:
        """ Get all customer information """
        if not self.is_connected:
            return []

        return list(self.collections[DBCollection.CUSTOMER].find())            

    def get_product_info(self) -> list:
        """ Get all product information """
        if not self.is_connected:
            return []

        return list(self.collections[DBCollection.PRODUCT].find())

if __name__=="__main__":
    db = MongoDBClient()
    db.check_connection()
