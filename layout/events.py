""" Event Module """


import qtawesome as qta
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QPushButton
from PyQt5.QtGui import QCloseEvent

from tools.common import InputMode
from tools.invoice_builder import InvoiceBuilder


class Events():
    """ Event class """
    def __init__(self, parent):
        self.parent = parent
        self.edit_row = None
        self.invoice_builder = InvoiceBuilder()

    def on_add_button_clicked(self):
        """ Event press add button """
        data = self.parent.top_layout.input_layout.get_data()
        status = self.parent.top_layout.input_layout.validate_all_data(data)
        if status is True:
            self.parent.top_layout.table_layout.add_row_to_table(data)
            self.parent.top_layout.input_layout.clear_all_data_input_field()

    def on_clear_button_clicked(self):
        """ Event press clear button """
        data = self.parent.top_layout.input_layout.get_data()
        if not any([value for _, value in data.items()]):
            return
        reply = QMessageBox.question(
            None,
            "Xác nhận",
            "Bạn có muốn hủy thay đổi?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.parent.top_layout.input_layout.clear_all_data_input_field()
            if self.parent.top_layout.input_layout.mode == InputMode.EDIT:
                self.parent.top_layout.table_layout.clean_table_color()
                self.parent.top_layout.input_layout.set_input_mode(mode=InputMode.ADD)
        else:
            return

    def on_save_button_clicked(self):
        """ Event press save button """
        data = self.parent.top_layout.input_layout.get_data()
        status = self.parent.top_layout.input_layout.validate_all_data(data)
        if status is True:
            self.parent.top_layout.table_layout.edit_data_by_row(self.edit_row, data)
            self.parent.top_layout.input_layout.clear_all_data_input_field()
            self.parent.top_layout.input_layout.set_input_mode(mode=InputMode.ADD)
            self.parent.top_layout.table_layout.clean_table_color()

    def on_table_clicked(self):
        """ Event double click on table """
        self.parent.top_layout.table_layout.clean_table_color()
        self.edit_row, edit_col = self.parent.top_layout.table_layout.get_current_cell()
        self.parent.top_layout.table_layout.highlight_edit_row(self.edit_row, edit_col)
        data = self.parent.top_layout.table_layout.get_data_by_row(self.edit_row)
        self.parent.top_layout.input_layout.set_data_to_input_field(data)
        self.parent.top_layout.input_layout.set_input_mode(mode=InputMode.EDIT)

    def on_export_button_clicked(self):
        """ Event clicked on export button """
        data = self.parent.top_layout.table_layout.get_table_data()
        path = self.invoice_builder.build(data)
        QMessageBox.information(
            None,
            "Xuất hóa đơn thành công",
            f"Hóa đơn được lưu tại:\n'{path}'"
        )
        self.parent.top_layout.table_layout.clean_table()

    def on_set_export_path_clicked(self):
        """ Event clicked on set export path """
        folder_path = QFileDialog.getExistingDirectory(None, "Select Folder", self.parent.config.export_folder)

        if folder_path:
            print(f"Selected folder: {folder_path}")
            self.parent.config.export_folder = folder_path
            self.parent.save_config()

    def on_close_app_clicked(self, event: QCloseEvent):
        """ Event clicked on close button """
        button_accept = QPushButton('Có')
        button_reject = QPushButton('Không')
        close_box = QMessageBox()

        close_icon = qta.icon('mdi6.close-thick', color='red')
        question_icon = qta.icon('fa5.question-circle', color='darkblue').pixmap(64, 64)
        close_box.setIconPixmap(question_icon)
        close_box.setWindowIcon(close_icon)

        close_box.setWindowTitle("Bạn có muốn đóng ứng dụng?")
        close_box.setText("Dữ liệu của phiên làm việc hiện tại sẽ bị xóa.\nNhấn 'Có' nếu bạn muốn đóng ứng dụng.")
        close_box.addButton(button_accept, QMessageBox.YesRole)
        close_box.addButton(button_reject, QMessageBox.NoRole)
        close_box.exec_()

        if close_box.clickedButton() == button_accept:
            event.accept()
        else:
            event.ignore()
