""" main module """


import sys

from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from tools.process_helper import start_broker


if __name__ == "__main__":
    start_broker()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
