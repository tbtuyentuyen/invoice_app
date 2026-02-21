""" Event Module """


import os

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QCloseEvent

from common.custom_widget import MessageBoxWidget
from common.constants import InputMode, MessageBoxType
from tools.invoice_builder import InvoiceBuilder
from tools.process_helper import stop_broker
from tools.utils import expand_env_vars_in_path


class Events():
    """ Event class """
    def __init__(self, parent):
        self.parent = parent

        self.edit_row = None
        self.invoice_builder = InvoiceBuilder()

    def on_clear_customer_clicked(self):
        """ Event press clear button on top layout """
        data = self.parent.customer_layout.get_data()
        if not any([value for _, value in data.items()]):
            return

        question_box = MessageBoxWidget(
            MessageBoxType.QUESTION,
            "Xác nhận",
            "Bạn có muốn xóa dữ liệu đang nhập?",
        )
        question_box.exec_()
        if question_box.clickedButton() == question_box.button_reject:
            return

        self.parent.customer_layout.clear_all_data_input_field()

    def on_add_product_clicked(self):
        """ Event press add button """
        data = self.parent.middle_layout.product_layout.get_data()
        status = self.parent.middle_layout.product_layout.validate_all_data(data)
        if status is True:
            self.parent.middle_layout.table_layout.add_row_to_table(data)
            self.parent.middle_layout.product_layout.clear_all_data_input_field()

    def on_clear_product_clicked(self):
        """ Event press clear button """
        data = self.parent.middle_layout.product_layout.get_data()
        if not any([value for _, value in data.items()]):
            return

        question_box = MessageBoxWidget(
            MessageBoxType.QUESTION,
            "Xác nhận",
            "Bạn có muốn xóa dữ liệu đang nhập?",
        )
        question_box.exec_()

        if question_box.clickedButton() == question_box.button_reject:
            return

        self.parent.middle_layout.product_layout.clear_all_data_input_field()

        # Switch back to add mode if currently in edit mode
        if self.parent.middle_layout.product_layout.mode == InputMode.EDIT:
            self.parent.middle_layout.table_layout.clean_table_color()
            self.parent.middle_layout.product_layout.set_input_mode(mode=InputMode.ADD)

    def on_update_product_clicked(self):
        """ Event press save button """
        data = self.parent.middle_layout.product_layout.get_data()
        status = self.parent.middle_layout.product_layout.validate_all_data(data)

        if status:
            # Update data on table
            self.parent.middle_layout.table_layout.edit_data_by_row(self.edit_row, data)

            # Switch back to add mode after saving
            self.parent.middle_layout.product_layout.clear_all_data_input_field()
            self.parent.middle_layout.table_layout.clean_table_color()
            self.parent.middle_layout.product_layout.set_input_mode(mode=InputMode.ADD)

    def on_table_clicked(self):
        """ Event double click on table """
        # Clear previous highlight
        self.parent.middle_layout.table_layout.clean_table_color()

        # Get current selected cell
        self.edit_row, edit_col = self.parent.middle_layout.table_layout.get_current_cell()
        self.parent.middle_layout.table_layout.highlight_edit_row(self.edit_row, edit_col)

        # Set data to input field and switch to edit mode
        data = self.parent.middle_layout.table_layout.get_data_by_row(self.edit_row)
        self.parent.middle_layout.product_layout.set_data_to_input_field(data)
        self.parent.middle_layout.product_layout.set_input_mode(mode=InputMode.EDIT)

    def on_export_button_clicked(self):
        """ Event clicked on export button """
        # Confirm export invoice
        question_box = MessageBoxWidget(
            MessageBoxType.QUESTION,
            "Xác nhận xuất hóa đơn",
            "Bạn có muốn xuất hóa đơn?",
        )
        question_box.exec_()
        if question_box.clickedButton() == question_box.button_reject:
            return

        # Collect customer data and invoice data
        customer_id, customer_data = self.parent.data_collectors.collect_customer_data()
        if not customer_data:
            return
        invoice_id, invoice_data = self.parent.data_collectors.collect_invoice_data(customer_id)
        if not invoice_data:
            return
        self.parent.parent.load_suggesion_data()

        # Build invoice
        try:
            pdf_path = self.invoice_builder.build(invoice_id, invoice_data, customer_data)
        except Exception as err: # pylint: disable=broad-exception-caught
            error_box = MessageBoxWidget(
                MessageBoxType.ERROR,
                "Xuất hóa đơn thất bại",
                f"Lỗi khi xuất hóa đơn: {err}"
            )
            error_box.exec_()
            return

        # Show success message
        info_box = MessageBoxWidget(
            MessageBoxType.INFO,
            "Xuất hóa đơn thành công",
            f"Hóa đơn được lưu tại:\n'{os.path.abspath(pdf_path)}'."
        )
        info_box.exec_()

        # Clear data on table and input field
        self.parent.middle_layout.table_layout.clean_table()
        self.parent.customer_layout.clear_all_data_input_field()

    def on_set_export_path_clicked(self):
        """ Event clicked on set export path """
        folder_path = QFileDialog.getExistingDirectory(
            None, "Select Folder", expand_env_vars_in_path(self.parent.config.export_folder)
        )

        if folder_path:
            self.parent.config.export_folder = folder_path
            self.parent.save_config()

    def on_close_app_clicked(self, event: QCloseEvent):
        """ Event clicked on close button """
        close_box = MessageBoxWidget(
            MessageBoxType.QUESTION,
            "Xác nhận đóng ứng dụng",
            "Dữ liệu của phiên làm việc hiện tại sẽ bị xóa.\nNhấn 'Có' nếu bạn muốn đóng ứng dụng."
        )
        close_box.exec_()

        if close_box.clickedButton() == close_box.button_accept:
            event.accept()
            stop_broker()
        else:
            event.ignore()
