""" Table Layout Module """


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLineEdit,
                             QTableWidgetItem, QHeaderView, QAbstractItemView, QLabel)

from common.styling import Style
from common.constants import TableAttribute
from common.custom_widget import QCustomTableWidget
from tools.utils import clear_format_money


class TableLayout(QVBoxLayout, Style):
    """ Table Layout class """
    def __init__(self, parent_view):
        super().__init__()
        self.parent_view = parent_view
        self.table_data = []

        self.col_dict = {
            TableAttribute.NAME: {'size': 0, 'align': Qt.AlignCenter},
            TableAttribute.QUANTITY: {'size': 120, 'align': Qt.AlignCenter},
            TableAttribute.TYPE: {'size': 120, 'align': Qt.AlignCenter},
            TableAttribute.PRICE: {'size': 180, 'align': Qt.AlignRight | Qt.AlignVCenter},
            TableAttribute.SUM: {'size': 180, 'align': Qt.AlignRight | Qt.AlignVCenter}
        }
        self.header_list = TableAttribute.list()
        self.table_widget = QCustomTableWidget(self)

        self.total_layout = QHBoxLayout()
        self.total_label = QLabel("Tổng tiền:")
        self.total_label.setObjectName('title_label')
        self.total_price = QLineEdit()
        self.total_price.setReadOnly(True)
        self.total_price.setObjectName('total_input')
        self.total_layout.addStretch()
        self.total_layout.addWidget(self.total_label)
        self.total_layout.addWidget(self.total_price)
        self.set_style(self.total_label)
        self.set_style(self.total_price)

        self.__config_table_widget()
        self.__init_ui()

    def __init_ui(self):
        self.addWidget(self.table_widget)
        self.addLayout(self.total_layout)

    def __config_table_widget(self):
        self.set_style(self.table_widget)
        self.table_widget.setColumnCount(len(self.header_list))
        self.table_widget.setRowCount(0)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.table_widget.setHorizontalHeaderLabels(self.header_list)
        for col, item in enumerate(TableAttribute):
            if size:=self.col_dict[item]['size']:
                self.table_widget.horizontalHeader().setSectionResizeMode(col, QHeaderView.Fixed)
                self.table_widget.setColumnWidth(col, size)
            else:
                self.table_widget.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)

        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def visualize_data(func):   # pylint: disable=no-self-argument
        """ Decorator fuction """
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.visualize_table_data()
        return wrapper

    def visualize_table_data(self):
        """ Visualize for table data """
        total = 0
        self.table_widget.setRowCount(len(self.table_data))
        for row, row_data in enumerate(self.table_data):
            for column, key in enumerate(row_data.keys()):
                if key in [TableAttribute.PRICE, TableAttribute.QUANTITY, TableAttribute.SUM]:
                    value = f"{int(row_data[key]):,}".replace(',', '.')
                else:
                    value = str(row_data[key])
                item = QTableWidgetItem(value)
                item.setTextAlignment(self.col_dict[key]['align'])
                self.table_widget.setItem(row, column, item)

                if key == TableAttribute.SUM:
                    total += int(row_data[key])

        self.total_price.setText(f"{total:,} VNĐ".replace(',', '.'))
        self.total_price.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    def get_current_cell(self):
        """ Get current cell """
        row = self.table_widget.selectedItems()[0].row()
        column = self.table_widget.selectedItems()[0].column()
        return row, column

    def get_table_data(self):
        """ Get all data from table """
        table_data = []
        for row in range(self.table_widget.rowCount()):
            row_data = {}
            for col, key in enumerate(TableAttribute):
                item = self.table_widget.item(row, col)
                if item is not None:
                    if key in [TableAttribute.PRICE, TableAttribute.SUM, TableAttribute.QUANTITY]:
                        row_data[key.value] = int(clear_format_money(item.text()))
                    else:
                        row_data[key.value] = item.text()
                else:
                    row_data[key.value] = ""
            table_data.append(row_data)
        return table_data

    def get_data_by_row(self, row: int):
        """ Get data by row """
        assert row < self.table_widget.rowCount(),\
            f"[ERROR] row must be < {self.table_widget.rowCount()}, got '{row}'"
        return self.get_table_data()[row]

    def highlight_edit_row(self, row, col):
        """ Highlight edit row """
        self.table_widget.item(row, col).setSelected(False)
        for col in range(self.table_widget.columnCount()):
            item = self.table_widget.item(row, col)
            if item:
                item.setBackground(QColor('#D0DDD0'))

    def clean_table_color(self):
        """ Clean table color to default """
        for row in range(self.table_widget.rowCount()):
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item:
                    item.setBackground(QColor('#EAEFEF'))

    @visualize_data
    def add_row_to_table(self, data: dict):
        """ Add sum column for data and new row to table """
        data[TableAttribute.SUM] = int(data[TableAttribute.QUANTITY])*int(data[TableAttribute.PRICE])
        self.table_data.append(data)

    @visualize_data
    def edit_data_by_row(self, row: int, data: dict):
        """ Edit data by row """
        self.table_data[row] = data

    @visualize_data
    def delete_data_by_row(self, checked_state : bool, row: int):  # pylint: disable=unused-argument
        """ Delete data by row """
        self.table_data.pop(row)

    @visualize_data
    def clean_table(self):
        """ Clean table data """
        self.table_data = []

    def lock_table(self, status: bool):
        """ Lock or unlock table """
        self.table_widget.setDisabled(status)
