""" Middle Layout Module """


from PyQt5.QtWidgets import QHBoxLayout, QWidget

from layout.table_layout import TableLayout
from layout.input_layout import InputLayout


class MiddleLayout(QHBoxLayout):
    """ Middle Layout class """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.table_widget = QWidget()
        self.table_layout = TableLayout(self)
        self.table_widget.setLayout(self.table_layout)

        self.input_widget = QWidget()
        self.input_layout = InputLayout(self)
        self.input_widget.setLayout(self.input_layout)
        self.input_widget.setFixedWidth(500)

        self.__init_ui()

    def __init_ui(self):
        self.addWidget(self.table_widget)
        self.addWidget(self.input_widget)
