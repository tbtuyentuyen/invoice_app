""" Top Layout Module """


from PyQt5.QtWidgets import QHBoxLayout, QWidget

from layout.events import Events
from layout.table_layout import TableLayout
from layout.input_layout import InputLayout


class TopLayout(QHBoxLayout):
    """ Top Layout class """
    def __init__(self):
        super().__init__()
        self.events = Events(self)

        self.table_widget = QWidget()
        self.table_layout = TableLayout(self)
        self.table_widget.setLayout(self.table_layout)

        self.input_widget = QWidget()
        self.input_layout = InputLayout(self)
        self.input_widget.setLayout(self.input_layout)
        self.input_widget.setFixedWidth(500)

        self.__init_ui()
        self.__connect_signals()

    def __init_ui(self):
        self.addWidget(self.table_widget)
        self.addWidget(self.input_widget)

    def __connect_signals(self):
        self.input_layout.add_button.clicked.connect(self.events.on_add_button_clicked)
        self.input_layout.clear_button.clicked.connect(self.events.on_clear_button_clicked)
        self.table_layout.table_widget.doubleClicked.connect(self.events.on_table_clicked)
