""" Main Layout Module """

from PyQt5.QtWidgets import QVBoxLayout

from layout.bottom_layout import BottomLayout
from layout.top_layout import TopLayout


class MainLayout(QVBoxLayout): # pylint:disable=R0903
    """ Main layout class """
    def __init__(self):
        super().__init__()
        self.top_layout = TopLayout()
        self.bottom_layout = BottomLayout()

        self.__init_ui()

    def __init_ui(self):
        self.addLayout(self.top_layout)
        self.addLayout(self.bottom_layout)
