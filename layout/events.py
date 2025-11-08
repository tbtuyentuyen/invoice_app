""" Event Module """


from PyQt5.QtWidgets import QMessageBox

from common import TableAttribute, InputMode


class Events():
    """ Event class """
    def __init__(self, parent):
        self.parent = parent
        self.edit_row = None

    def on_add_button_clicked(self):
        """ Event press add button """
        # data = self.parent.input_layout.get_data()
        data = {TableAttribute.NAME: 'f', TableAttribute.QUANTITY: '4', TableAttribute.TYPE: 'fhd', TableAttribute.PRICE: '7'}
        status = self.parent.input_layout.validate_all_data(data)
        if status is True:
            self.parent.table_layout.add_row_to_table(data)
            self.parent.input_layout.clear_all_data_input_field()

    def on_clear_button_clicked(self):
        """ Event press clear button """
        reply = QMessageBox.question(
            None,
            "Xác nhận",
            "Bạn có muốn hủy thay đổi?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.parent.input_layout.clear_all_data_input_field()
            if self.parent.input_layout.mode == InputMode.EDIT:
                self.parent.input_layout.set_input_mode(mode=InputMode.ADD)
        else:
            return

    def on_save_button_clicked(self):
        """ Event press save button """
        data = self.parent.input_layout.get_data()
        status = self.parent.input_layout.validate_all_data(data)
        if status is True:
            self.parent.table_layout.edit_data_by_row(self.edit_row, data)
            self.parent.input_layout.clear_all_data_input_field()
            self.parent.input_layout.set_input_mode(mode=InputMode.ADD)
            self.parent.table_layout.clean_table_color()

    def on_table_clicked(self):
        """ Event double click on table """
        self.parent.table_layout.clean_table_color()
        self.edit_row, edit_col = self.parent.table_layout.get_current_cell()
        print(self.edit_row, edit_col)
        self.parent.table_layout.highlight_edit_row(self.edit_row, edit_col)
        data = self.parent.table_layout.get_data_by_row(self.edit_row)
        self.parent.input_layout.set_data_to_input_field(data)
        self.parent.input_layout.set_input_mode(mode=InputMode.EDIT)
