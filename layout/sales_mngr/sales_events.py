""" Sales Events Module """


import os

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

from tools.invoice_builder import InvoiceBuilder
from common.app_context import AppContext
from common.custom_widget import MessageBoxWidget
from common.constants import InputMode, MessageBoxType


class SalesEvents():
    """ Sales Events class """
    def __init__(self, parent_view):
        self.parent_view = parent_view
        self.context: AppContext = parent_view.context
        self.edit_row = None
        self.invoice_builder = InvoiceBuilder()

    def on_clear_customer_clicked(self):
        """ Event press clear button on top layout """
        data = self.parent_view.customer_layout.get_data()
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

        self.parent_view.customer_layout.clear_all_data_input_field()

    def on_add_product_clicked(self):
        """ Event press add button """
        data = self.parent_view.middle_layout.product_layout.get_data()
        status = self.parent_view.middle_layout.product_layout.validate_all_data(data)
        if status is True:
            self.parent_view.middle_layout.table_layout.add_row_to_table(data)
            self.parent_view.middle_layout.product_layout.clear_all_data_input_field()

    def on_clear_product_clicked(self):
        """ Event press clear button """
        data = self.parent_view.middle_layout.product_layout.get_data()
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

        self.parent_view.middle_layout.product_layout.clear_all_data_input_field()

        # Switch back to add mode if currently in edit mode
        if self.parent_view.middle_layout.product_layout.mode == InputMode.EDIT:
            self.parent_view.middle_layout.table_layout.clean_table_color()
            self.parent_view.middle_layout.product_layout.set_input_mode(mode=InputMode.ADD)

    def on_update_product_clicked(self):
        """ Event press save button """
        data = self.parent_view.middle_layout.product_layout.get_data()
        status = self.parent_view.middle_layout.product_layout.validate_all_data(data)

        if status:
            # Update data on table
            self.parent_view.middle_layout.table_layout.edit_data_by_row(self.edit_row, data)

            # Switch back to add mode after saving
            self.parent_view.middle_layout.product_layout.clear_all_data_input_field()
            self.parent_view.middle_layout.table_layout.clean_table_color()
            self.parent_view.middle_layout.product_layout.set_input_mode(mode=InputMode.ADD)

    def on_table_clicked(self):
        """ Event double click on table """
        # Clear previous highlight
        self.parent_view.middle_layout.table_layout.clean_table_color()

        # Get current selected cell
        self.edit_row, edit_col = self.parent_view.middle_layout.table_layout.get_current_cell()
        self.parent_view.middle_layout.table_layout.highlight_edit_row(self.edit_row, edit_col)

        # Set data to input field and switch to edit mode
        data = self.parent_view.middle_layout.table_layout.get_data_by_row(self.edit_row)
        self.parent_view.middle_layout.product_layout.set_data_to_input_field(data)
        self.parent_view.middle_layout.product_layout.set_input_mode(mode=InputMode.EDIT)

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
        customer_id, customer_data = self.parent_view.data_collectors.collect_customer_data()
        if not customer_data:
            return
        invoice_id, invoice_data = self.parent_view.data_collectors.collect_invoice_data(customer_id)
        if not invoice_data:
            return
        self.parent_view.load_suggesion_data()

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
            f'Hóa đơn được lưu tại:\n{os.path.abspath(pdf_path)}'
        )

        open_btn.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))
        )

        # Clear data on table and input field
        self.parent_view.middle_layout.table_layout.clean_table()
        self.parent_view.customer_layout.clear_all_data_input_field()
