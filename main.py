""" main module """


import sys

from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from tools.mongodb_client import MongoDBClient
from common.loading_widget import LoadingWidget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mongodb_client = MongoDBClient()
    loading_widget = LoadingWidget(mongodb_client)
    window = MainWindow(mongodb_client)

    loading_widget.start_loading(window.show)

    sys.exit(app.exec_())
