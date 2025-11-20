""" main module """


import sys
import qtawesome as qta

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QThread

from layout.menu_bar import MenuBar
from layout.main_layout import MainLayout
from tools.mongodb_client import MongoDBWorker
from tools.common import MongoDBStatus


class MainWindow(QMainWindow): # pylint:disable=R0903
    """ Main Window class """
    def __init__(self):
        super().__init__()
        self.main_layout = MainLayout(self)
        self.__config_window()
        self.__init_ui()

        self.mongodb_thread = None
        self.mongodb_client = None
        self.mongodb_worker = None
        self.check_mongodb_connection()
 

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

    def change_mongodb_status(self, status: str):
        """ change mongodb status function """
        self.__change_status_bar(status)
        self.mongodb_thread.quit()
        self.mongodb_thread.wait()
        self.mongodb_thread.deleteLater()
        del self.mongodb_thread
        self.mongodb_thread = None
        self.mongodb_client = self.mongodb_worker.mongodb_client
        self.mongodb_worker.deleteLater()

    def check_mongodb_connection(self):
        """ Check MongoDB connection """
        self.__change_status_bar(MongoDBStatus.CONNECTING.value)
        self.mongodb_thread = QThread()
        self.mongodb_worker = MongoDBWorker()
        self.mongodb_worker.moveToThread(self.mongodb_thread)
        self.mongodb_worker.finished.connect(self.change_mongodb_status)
        self.mongodb_thread.started.connect(self.mongodb_worker.start_connection)
        self.mongodb_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
