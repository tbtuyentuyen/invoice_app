""" Shop config dialog """

from PyQt5.QtWidgets import QDialog, QVBoxLayout

from common.app_context import AppContext
from layout.visualize_layout.invoice_visualize import InvoiceVisualize

class ShopConfigDialog(QDialog):
    """ Dialog to edit shop config """
    def __init__(self, parent_view):
        super().__init__()
        self.context: AppContext = parent_view.context
        self.setWindowTitle("Thông tin cửa hàng")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        self.visualize = InvoiceVisualize(parent_view)
        layout.addWidget(self.visualize)

        self.setLayout(layout)
