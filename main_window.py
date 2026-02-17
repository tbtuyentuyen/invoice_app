""" Main Window module """


import os
import qtawesome as qta

from PyQt5.QtWidgets import QMainWindow, QWidget

from layout.menu_bar.menu_bar import MenuBar
from layout.main_layout import MainLayout
from common.constants import MongoDBStatus
from tools.mongodb_client import MongoDBClient

INVOICE_APP_PATH = os.environ['INVOICE_APP_PATH']

class MainWindow(QMainWindow): # pylint:disable=R0903
    """ Main Window class """
    def __init__(self, mongodb_client: MongoDBClient):
        super().__init__()
        self.mongodb_client = MongoDBClient()
        self.main_layout = MainLayout(self)
        self.__config_window()

        self.mongodb_client = mongodb_client
        self.mongodb_client.finish_signal.connect(self.__change_status_bar)
        self.mongodb_client.finish_signal.connect(self.load_suggesion_data)

        self.__init_ui()

    def __init_ui(self):
        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)
        self.__change_status_bar(MongoDBStatus.UNKNOWN.value)

    def __config_window(self):
        app_icon = qta.icon('ph.table', color='green')
        self.setWindowTitle("App")
        self.setWindowIcon(app_icon)
        self.setGeometry(0, 0, 1500, 700)

        self.closeEvent = self.main_layout.events.on_close_app_clicked  # pylint: disable=invalid-name

    def __change_status_bar(self, status: str) -> None:
        self.statusBar().showMessage(f"MongoDB: {status}")

    def resizeEvent(self, event): # pylint: disable=invalid-name
        """ resize event"""
        self.main_layout.customer_layout.on_window_resize(self.width())
        super().resizeEvent(event)

    def load_suggesion_data(self, status: str = None) -> None:   # pylint: disable=unused-argument
        """ Load suggestion data """
        customers_data = self.mongodb_client.get_customer_info()
        self.main_layout.customer_layout.load_data_suggestion(customers_data)

        products_data = self.mongodb_client.get_product_info()
        self.main_layout.middle_layout.product_layout.load_data_suggestion(products_data)
