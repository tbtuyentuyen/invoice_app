""" MongoDB Client """


import os

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from PyQt5.QtCore import QObject, pyqtSignal

from tools.common import MongoDBStatus
from tools.utils import load_json, save_json

CONFIG_PATH = os.environ['CONFIG_PATH']


class MongoDBWorker(QObject):
    """ MongoDB worker"""
    finished = pyqtSignal(str)

    def __init__(self, mongo_client):
        super().__init__()
        self.mongodb_client = mongo_client

    def start_connection(self):
        """ Start connection function """
        if self.mongodb_client.check_connection():
            status = MongoDBStatus.CONNECTED.value
        else:
            status = MongoDBStatus.DISCONNECTED.value

        self.finished.emit(status)


class MongoDBClient:
    """ Mongo Database Client """
    def __init__(self):
        self.config = load_json(CONFIG_PATH)
        self.client = MongoClient(
            self.config.mongodb_endpoint,
            timeoutMS=self.config.mongodb_timeout,
            socketTimeoutMS=self.config.mongodb_timeout,
            connectTimeoutMS=self.config.mongodb_timeout
        )
        database = self.client["invoice_app"]
        self.invoice_col = database["invoices"]
        self.offline_mode = True

        os.makedirs(self.config.backup_folder, exist_ok=True)

    def check_connection(self):
        """ Check connect to MongoDB """
        try:
            self.client.server_info()
            self.offline_mode = False
            return True
        except ServerSelectionTimeoutError:
            self.offline_mode = True
            return False
        except Exception:  # pylint: disable=broad-exception-caught
            self.offline_mode = True
            return False

    def disconnect_client(self):
        """ Disconnect to MongoDB"""
        if not self.offline_mode:
            self.client.close()

    def get_id_invoice(self, data: dict) -> str:
        """ Get id of specific invoice """
        if not self.offline_mode:
            doc = self.invoice_col.find_one(data)
            if doc:
                return str(doc["_id"])

    def add_invoice(self, data_id: str, data: list) -> bool|str:
        """ Insert one invoice to collection """
        data_dict = {'_id': data_id, 'data': data}

        if not self.offline_mode:
            self.invoice_col.insert_one(data_dict)
            return True
        else:
            save_path = os.path.join(self.config.backup_folder, f"{data_id}.json")
            save_json(data_dict, save_path)
            return save_path

    def delete_invoice(self, data: dict) -> None:
        """ Delete one invoice out of collection """
        if not self.offline_mode:
            self.invoice_col.delete_one(data)

    def modify_invoice(self, id_invoice: str, new_invoice: dict) -> None:
        """ Modify invoice infomation """
        if not self.offline_mode:
            self.invoice_col.update_one(
                {"_id": id_invoice},
                {'$set': new_invoice}
            )

    def query_invoice_name(self):
        """ Query invoice by name """
        if not self.offline_mode:
            self.invoice_col.find({}, {"name": 1, "_id": 0 })


if __name__=="__main__":
    db = MongoDBClient()
    db.check_connection()
