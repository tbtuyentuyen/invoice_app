""" Main Layout Module """

import os

from PyQt5.QtWidgets import QVBoxLayout

from layout.events import Events
from layout.bottom_layout import BottomLayout
from layout.middle_layout import MiddleLayout
from tools.utils import load_json, save_json


CONFIG_PATH = os.environ['CONFIG_PATH']

class MainLayout(QVBoxLayout): # pylint:disable=R0903
    """ Main layout class """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.config = load_json(CONFIG_PATH)

        self.events = Events(self)
        self.middle_layout = MiddleLayout(self)
        self.bottom_layout = BottomLayout()

        self.__init_ui()
        self.__connect_signals()

    def __init_ui(self):
        self.addLayout(self.middle_layout)
        self.addLayout(self.bottom_layout)

    def __connect_signals(self):
        self.middle_layout.input_layout.add_button.clicked.connect(self.events.on_add_button_clicked)
        self.middle_layout.input_layout.clear_button.clicked.connect(self.events.on_clear_button_clicked)
        self.middle_layout.table_layout.table_widget.doubleClicked.connect(self.events.on_table_clicked)
        self.bottom_layout.export_button.clicked.connect(self.events.on_export_button_clicked)

    def save_config(self):
        """ Save config """
        save_json(self.config, CONFIG_PATH)
