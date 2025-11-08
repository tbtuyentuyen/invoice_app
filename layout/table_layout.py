""" Table Layout Module """


from PyQt5 import QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QMenu

from layout.styling import Style
from common import TableAttribute


class CustomTableWidget(QTableWidget):
    """ Custom table widget class """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            item = self.itemAt(event.pos())
            if item:
                menu = QMenu(self)
                delete_action = menu.addAction("Xóa hàng")
                delete_action.triggered.connect(lambda checked_state: self.parent.delete_data_by_row(checked_state, item.row()))
                menu.exec_(event.globalPos())
            else:
                return
        super().mousePressEvent(event)


class TableLayout(QVBoxLayout, Style):
    """ Table Layout class """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.table_data = []

        self.header_list = TableAttribute.list()
        self.table_widget = CustomTableWidget(self)

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
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def __get_table_data(self):
        data = []
        for row in range(self.table_widget.rowCount()):
            row_data = []
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)
        return data

    def visualize_data(func):   # pylint: disable=no-self-argument
        """ Decorator fuction """
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.visualize_table_data()
        return wrapper

    def visualize_table_data(self):
        """ Visualize for table data """
        self.table_widget.setRowCount(len(self.table_data))
        for row, row_data in enumerate(self.table_data):
            for column, key in enumerate(row_data.keys()):
                item = QTableWidgetItem(str(row_data[key]))
                self.table_widget.setItem(row, column, item)
                self.table_widget.resizeColumnsToContents()
                self.table_widget.resizeRowsToContents()

    def get_current_cell(self):
        """ Get current cell """
        row = self.table_widget.selectedItems()[0].row()
        column = self.table_widget.selectedItems()[0].column()
        return row, column

    def get_data_by_row(self, row: int):
        """ Get data by row """
        assert row < self.table_widget.rowCount(),\
            f"[ERROR] row must be < {self.table_widget.rowCount()}, got '{row}'"

        data_dict = {}
        table_data = self.__get_table_data()
        for i, key in enumerate(TableAttribute):
            data_dict[key] = table_data[row][i]

        return data_dict

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
        """ Add new row to table """
        self.table_data.append(data)

    @visualize_data
    def edit_data_by_row(self, row: int, data: dict):
        """ Edit data by row """
        self.table_data[row] = data

    @visualize_data
    def delete_data_by_row(self, checked_state : bool, row: int):
        """ Delete data by row """
        self.table_data.pop(row)
