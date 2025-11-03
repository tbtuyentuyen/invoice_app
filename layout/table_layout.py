""" Table Layout Module """


from PyQt5.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView

from layout.styling import Style
from common import TableAttribute


class TableLayout(QVBoxLayout, Style):
    """ Table Layout class """
    def __init__(self):
        super().__init__()

        self.header_list = TableAttribute.list()
        self.table_widget = QTableWidget()

        self.__config_table_widget()
        self.__init_ui()

    def __init_ui(self):
        self.addWidget(self.table_widget)

    def __config_table_widget(self):
        self.set_style(self.table_widget)
        self.table_widget.setColumnCount(len(self.header_list))
        self.table_widget.setRowCount(0)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_widget.setHorizontalHeaderLabels(self.header_list)

    def add_row_to_table(self, data: dict):
        """ Add new row to table """
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)
        for column, key in enumerate(data.keys()):
            item = QTableWidgetItem(str(data[key]))
            self.table_widget.setItem(row_position, column, item)
            self.table_widget.resizeColumnsToContents()
            self.table_widget.resizeRowsToContents()
