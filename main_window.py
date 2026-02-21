""" Main Window module """


import os
import qtawesome as qta

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from layout.main_tab_widget import MainTabWidget
from layout.menu_bar.menu_bar import MenuBar
from layout.events import Events
from common.constants import MongoDBStatus


class MainWindow(QMainWindow): # pylint:disable=R0903
    """ Main Window class """
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.events = Events(parent_view=self)

        self.main_layout = QVBoxLayout()
        self.tab_widget = MainTabWidget(context=self.context)
        self.__config_window()

        self.context.mongodb_client.finish_signal.connect(self.__change_status_bar)
        self.context.mongodb_client.finish_signal.connect(self.tab_widget.sales_management_tab.load_suggesion_data)

        self.__init_ui()

    def __init_ui(self):
        menu_bar = MenuBar(parent_view=self)
        self.setMenuBar(menu_bar)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)
        self.__change_status_bar(MongoDBStatus.UNKNOWN.value)

        self.main_layout.addWidget(self.tab_widget)

    def __config_window(self):
        app_icon = qta.icon('ph.table', color='green')
        self.setWindowTitle("App")
        self.setWindowIcon(app_icon)
        self.setGeometry(0, 0, 1500, 700)

    def __change_status_bar(self, status: str) -> None:
        self.statusBar().showMessage(f"MongoDB: {status}")

    def closeEvent(self, event):    # pylint: disable=invalid-name
        """ Event close app """
        self.events.handle_close(event)

    def resizeEvent(self, event): # pylint: disable=invalid-name
        """ resize event"""
        self.tab_widget.sales_management_tab.handle_resize(self.width())
        super().resizeEvent(event)
