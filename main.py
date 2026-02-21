""" main module """


import sys

from PyQt5.QtWidgets import QApplication


from main_window import MainWindow
from common.app_context import AppContext
from common.loading_widget import LoadingWidget
from tools.utils import generate_config_folder

if __name__ == "__main__":
    generate_config_folder()
    app = QApplication(sys.argv)
    context = AppContext()
    loading_widget = LoadingWidget(context=context)
    window = MainWindow(context=context)

    loading_widget.start_loading(window.show)

    sys.exit(app.exec_())
