""" Event Module """


import os
from datetime import datetime

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QCloseEvent

from tools.common import InputMode, CustomerAttribute, MessageBoxType, DBCollection, TableAttribute
from tools.invoice_builder import InvoiceBuilder
from tools.process_helper import stop_broker
from tools.utils import expand_env_vars_in_path, encode_product_id
from layout.custom_widget import MessageBoxWidget


class Events():
    """ Event class """
    def __init__(self, parent):
        self.parent = parent
        self.edit_row = None
        self.invoice_builder = InvoiceBuilder()

    def on_clear_button_top_layout_clicked(self):
        """ Event press clear button on top layout """
        data = self.parent.top_layout.get_data()
        if not any([value for _, value in data.items()]):
            return

        question_box = MessageBoxWidget(
            MessageBoxType.QUESTION,
            "Xác nhận",
            "Bạn có muốn xóa dữ liệu đang nhập?",
        )
        question_box.exec_()
        if question_box.clickedButton() == question_box.button_accept:
            self.parent.top_layout.clear_all_data_input_field()
        else:
            return

    def on_add_button_clicked(self):
        """ Event press add button """
        data = self.parent.middle_layout.input_layout.get_data()
        status = self.parent.middle_layout.input_layout.validate_all_data(data)
        if status is True:
            self.parent.middle_layout.table_layout.add_row_to_table(data)
            self.parent.middle_layout.input_layout.clear_all_data_input_field()

    def on_clear_button_clicked(self):
        """ Event press clear button """
        data = self.parent.middle_layout.input_layout.get_data()
        if not any([value for _, value in data.items()]):
            return

        question_box = MessageBoxWidget(
            MessageBoxType.QUESTION,
            "Xác nhận",
            "Bạn có muốn xóa dữ liệu đang nhập?",
        )
        question_box.exec_()
        if question_box.clickedButton() == question_box.button_accept:
            self.parent.middle_layout.input_layout.clear_all_data_input_field()
            if self.parent.middle_layout.input_layout.mode == InputMode.EDIT:
                self.parent.middle_layout.table_layout.clean_table_color()
                self.parent.middle_layout.input_layout.set_input_mode(mode=InputMode.ADD)
        else:
            return

    def on_save_button_clicked(self):
        """ Event press save button """
        data = self.parent.middle_layout.input_layout.get_data()
        status = self.parent.middle_layout.input_layout.validate_all_data(data)
        if status is True:
            self.parent.middle_layout.table_layout.edit_data_by_row(self.edit_row, data)
            self.parent.middle_layout.input_layout.clear_all_data_input_field()
            self.parent.middle_layout.input_layout.set_input_mode(mode=InputMode.ADD)
            self.parent.middle_layout.table_layout.clean_table_color()

    def on_table_clicked(self):
        """ Event double click on table """
        self.parent.middle_layout.table_layout.clean_table_color()
        self.edit_row, edit_col = self.parent.middle_layout.table_layout.get_current_cell()
        self.parent.middle_layout.table_layout.highlight_edit_row(self.edit_row, edit_col)
        data = self.parent.middle_layout.table_layout.get_data_by_row(self.edit_row)
        self.parent.middle_layout.input_layout.set_data_to_input_field(data)
        self.parent.middle_layout.input_layout.set_input_mode(mode=InputMode.EDIT)

    def on_export_button_clicked(self):
        """ Event clicked on export button """
        customer_data = self.parent.top_layout.get_data()
        customer_sts = self.parent.top_layout.validate_all_data(customer_data)
        invoice_data = self.parent.middle_layout.table_layout.get_table_data()
        if invoice_data and customer_sts:
            question_box = MessageBoxWidget(
                MessageBoxType.QUESTION,
                "Xác nhận xuất hóa đơn",
                "Bạn có muốn xuất hóa đơn?",
            )
            question_box.exec_()
            if question_box.clickedButton() == question_box.button_reject:
                return
            mongodb_client = self.parent.parent.mongodb_client

            # Customer
            customer_id = customer_data[CustomerAttribute.PHONE_NUMBER.value]
            customer_data.update({
                "_id": customer_id
            })
            customer_result = mongodb_client.add_document(customer_data, DBCollection.CUSTOMER)
            self.parent.top_layout.user_suggestion[customer_id] = customer_data

            # Product
            invoice_list = []
            for item in invoice_data:
                product_id = encode_product_id(
                    item[TableAttribute.NAME.value],
                    item[TableAttribute.TYPE.value]
                )
                product = {
                    "_id": product_id,
                    TableAttribute.NAME.value: item[TableAttribute.NAME.value],
                    TableAttribute.TYPE.value: item[TableAttribute.TYPE.value],
                    TableAttribute.PRICE.value: item[TableAttribute.PRICE.value],
                }
                mongodb_client.add_document(product, DBCollection.PRODUCT)
                invoice_list.append({
                    "product_id": product_id,
                    "quantity": item[TableAttribute.QUANTITY.value],
                    "sum": item[TableAttribute.SUM.value],
                })

            self.parent.parent.load_suggesion_data()

            # Invoice
            invoice_id = f'invoice_{datetime.now().strftime("%y%m%d_%H%M%S")}'
            invoice = {
                "_id": invoice_id,
                "data": invoice_list,
                "customer_id": customer_id,
                "updated_at": datetime.now()
            }
            invoice_result = mongodb_client.add_document(invoice, DBCollection.INVOICE)

            if isinstance(invoice_result, bool) and isinstance(customer_result, bool):
                print("[INFO] Thông tin hóa đơn đã được tải lên database.")
            else:
                print(f"[INFO] Thông tin hóa đơn đã được lưu tại: '{customer_result}' và {invoice_result}'")

            try:
                pdf_path = self.invoice_builder.build(invoice_id, invoice_data, customer_data)
            except Exception as err: # pylint: disable=broad-exception-caught
                print(f"[ERROR] Xuất hóa đơn thất bại: {err}")
                return
            
            info_box = MessageBoxWidget(
                MessageBoxType.INFO,
                "Xuất hóa đơn thành công",
                f"Hóa đơn được lưu tại:\n'{os.path.abspath(pdf_path)}'."
            )
            info_box.exec_()
            self.parent.middle_layout.table_layout.clean_table()
            self.parent.top_layout.clear_all_data_input_field()
        else:
            warning_box = MessageBoxWidget(
                MessageBoxType.WARNING,
                "Xuất hóa đơn thất bại",
                "Xin điền thông hóa đơn hoặc người mua trước khi xuất hóa đơn!"
            )
            warning_box.exec_()

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
