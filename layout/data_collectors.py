""" Data Collector Module """


import copy
from datetime import datetime

from common.constants import CustomerAttribute, DBCollection, MessageBoxType, TableAttribute
from common.custom_widget import MessageBoxWidget
from common.app_context import AppContext
from tools.utils import encode_product_id


class DataCollectors:
    """ Class collect data from all input field and validate data before save to database """

    def __init__(self, parent_view):
        self.parent_view = parent_view
        self.context: AppContext = self.parent_view.context

    def _upload_to_database(self, data: dict|list, collection_name: list) -> bool:
        """ Upload data to database """
        sts = self.context.mongodb_client.add_document(data, collection_name)
        if not sts:
            error_box = MessageBoxWidget(
                MessageBoxType.ERROR,
                "Lỗi lưu dữ liệu",
                f"Không thể lưu dữ liệu vào database {collection_name.name.lower()}. Vui lòng thử lại sau!"
            )
            error_box.exec_()
            return False
        return True

    def _upload_customer_data(self, customer_id: str, customer_data: dict) -> bool:
        """ Upload customer data to database """
        customer_data.update({
            "_id": customer_id
        })
        return self._upload_to_database(customer_data, DBCollection.CUSTOMER)

    def _upload_invoice_data(self, invoice_id: str, products: list, customer_id: str) -> bool:
        """ Upload invoice data to database """
        invoice = {
            "_id": invoice_id,
            "data": products,
            "customer_id": customer_id,
            "updated_at": datetime.now()
        }
        return self._upload_to_database(invoice, DBCollection.INVOICE)

    def _build_invoice_by_product_data(self, invoice_data: list) -> list:
        """ Collect product data from table """
        products = []
        for item in invoice_data:
            product_id = self.collect_product_data(item)
            if not product_id:
                return None
            products.append({
                "product_id": product_id,
                "quantity": item[TableAttribute.QUANTITY.value],
                "sum": item[TableAttribute.SUM.value],
            })
        return products

    def collect_product_data(self, invoice_item: dict) -> str:
        """ Collect product data from invoice data """
        product_id = encode_product_id(
            invoice_item[TableAttribute.NAME.value],
            invoice_item[TableAttribute.TYPE.value]
        )
        product = {
            "_id": product_id,
            TableAttribute.NAME.value: invoice_item[TableAttribute.NAME.value],
            TableAttribute.TYPE.value: invoice_item[TableAttribute.TYPE.value],
            TableAttribute.PRICE.value: invoice_item[TableAttribute.PRICE.value],
        }
        if not self._upload_to_database(product, DBCollection.PRODUCT):
            return None
        return product_id

    def collect_customer_data(self) -> tuple[str, dict]:
        """ Collect customer data from input field """
        # Get customer data from input field
        customer_data = self.parent_view.customer_layout.get_data()

        # Validate customer data
        if not self.parent_view.customer_layout.validate_all_data(customer_data):
            warning_box = MessageBoxWidget(
                MessageBoxType.WARNING,
                "Xuất hóa đơn thất bại",
                "Xin điền người mua trước khi xuất hóa đơn!"
            )
            warning_box.exec_()
            return (None, None)

        # Upload customer data to database
        customer_id = customer_data[CustomerAttribute.PHONE_NUMBER.value]
        if not self._upload_customer_data(customer_id, copy.deepcopy(customer_data)):
            return (None, None)

        # Set customer data to user suggestion
        self.parent_view.customer_layout.user_suggestion[customer_id] = customer_data

        return (customer_id, customer_data)

    def collect_invoice_data(self, customer_id:str) -> tuple[str, list]:
        """ Collect invoice data from table """
        # Get invoice data from table
        invoice_data = self.parent_view.middle_layout.table_layout.get_table_data()

        # Validate invoice data
        if not invoice_data:
            warning_box = MessageBoxWidget(
                MessageBoxType.WARNING,
                "Xuất hóa đơn thất bại",
                "Xin điền thông tin sản phẩm trước khi xuất hóa đơn!"
            )
            warning_box.exec_()
            return (None, None)

        # Build invoice data by product data
        invoice_id = f'invoice_{datetime.now().strftime("%y%m%d_%H%M%S")}'
        products = self._build_invoice_by_product_data(invoice_data)
        if not products:
            return (None, None)

        # Upload invoice data to database
        if not self._upload_invoice_data(invoice_id, products , customer_id):
            return (None, None)

        return (invoice_id, invoice_data)
