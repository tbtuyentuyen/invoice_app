""" main module """


import sys
import qtawesome as qta

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from layout.menu_bar import MenuBar
from layout.main_layout import MainLayout


class MainWindow(QMainWindow): # pylint:disable=R0903
    """ Main Window class """
    def __init__(self):
        super().__init__()
        self.main_layout = MainLayout()
        self.__config_window()
        self.__init_ui()

    def __init_ui(self):
        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def __config_window(self):
        app_icon = qta.icon('ph.table', color='green')
        self.setWindowTitle("App")
        self.setWindowIcon(app_icon)
        self.setGeometry(0, 0, 1500, 700)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
