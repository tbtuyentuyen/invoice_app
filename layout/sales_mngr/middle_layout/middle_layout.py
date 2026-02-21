""" Middle Layout Module """


from PyQt5.QtWidgets import QHBoxLayout, QWidget

from layout.sales_mngr.middle_layout.table_layout import TableLayout
from layout.sales_mngr.middle_layout.product_layout import ProductLayout

class MiddleLayout(QHBoxLayout):
    """ Middle Layout class """
    def __init__(self, parent_view):
        super().__init__()
        self.parent_view = parent_view

        self.table_widget = QWidget()
        self.table_layout = TableLayout(self)
        self.table_widget.setLayout(self.table_layout)

        self.input_widget = QWidget()
        self.product_layout = ProductLayout(self)
        self.input_widget.setLayout(self.product_layout)
        self.input_widget.setFixedWidth(500)

        self.__init_ui()

    def __init_ui(self):
        self.addWidget(self.table_widget)
        self.addWidget(self.input_widget)
