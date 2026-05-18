""" Visualize invoice """
import os
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout, 
    QLineEdit,
    QLabel,
    QWidget,
    QFrame,
    QGridLayout
)

from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

from common.app_context import AppContext
from common.constants import CustomerAttribute, InvoiceFontSize
from tools.utils import expand_env_vars_in_path

items = [
    {
        "name": "item 1",
        "unit": "unit 1",
        "qty": 1,
        "price": 5000
    },
    {
        "name": "item 2",
        "unit": "unit 2",
        "qty": 2,
        "price": 10000
    }
]

class InvoiceVisualize(QWidget):
    """ Visualize invoice layout """
    def __init__(self, parent_view=None):
        super().__init__()
        if parent_view is not None:
            self.context: AppContext = parent_view.context
        else:
            self.context = AppContext()
        self.shop_config = self.context.shop_config

        self.__init_ui()

    def __init_ui(self):
        self.setFixedSize(800, 800)
        self.visualize_layout = QVBoxLayout()
        self._build_shop_layout()
        self._build_customer_layout()
        self._build_invoice_layout()
        self._build_signature_layout()
        self.setLayout(self.visualize_layout)

    def _build_shop_layout(self):
        def _add_shop_item(layout, text, font, alignment=Qt.AlignCenter):
            item_widget = QLabel(text)
            item_widget.setFont(font)
            warp_layout = QHBoxLayout()
            warp_layout.addWidget(item_widget, alignment=alignment)
            layout.addLayout(warp_layout)

        shop_layout = QHBoxLayout()
        left_section = QVBoxLayout()
        _add_shop_item(
            left_section,
            self.shop_config["shop_title"],
            QFont("Arial", InvoiceFontSize.NORMAL.value, QFont.Bold),
        )
        _add_shop_item(
            left_section,
            self.shop_config["shop_name"],
            QFont("Arial", InvoiceFontSize.BIG.value, QFont.Bold),
        )
        _add_shop_item(
            left_section,
            self.shop_config["shop_address"],
            QFont("Arial", InvoiceFontSize.NORMAL.value),
        )
        _add_shop_item(
            left_section,
            self.shop_config["shop_phone"],
            QFont("Arial", InvoiceFontSize.NORMAL.value, QFont.Bold),
        )
        _add_shop_item(
            left_section,
            self.shop_config["shop_bank"],
            QFont("Arial", InvoiceFontSize.NORMAL.value, QFont.Bold),
        )
        _add_shop_item(
            left_section,
            self.shop_config["shop_owner"],
            QFont("Arial", InvoiceFontSize.NORMAL.value, QFont.Bold),
        )

        right_section = QVBoxLayout()
        _add_shop_item(
            right_section,
            self.shop_config["shop_specialty"],
            QFont("Arial", InvoiceFontSize.HEADER.value, QFont.Bold),
        )
        _add_shop_item(
            right_section,
            f"{self.shop_config['invoice_title']} {self.shop_config['invoice_number']}",
            QFont("Arial", InvoiceFontSize.HEADER.value, QFont.Bold),
        )

        shop_layout.addLayout(left_section)
        shop_layout.addStretch()
        shop_layout.addLayout(right_section)
        self.visualize_layout.addLayout(shop_layout)

    def _build_customer_layout(self):
        def _add_customer_item(layout, text, font):
            item_widget = QLabel(text)
            item_widget.setFont(font)
            warp_layout = QHBoxLayout()
            warp_layout.addWidget(item_widget, alignment=Qt.AlignLeft)
            layout.addLayout(warp_layout)

        def _add_line(layout):
            line_frame = QFrame()
            line_frame.setFrameShape(QFrame.HLine)
            line_frame.setStyleSheet("color: black; background-color: black; height: 2px;")
            line_frame.setFixedHeight(2)
            layout.addWidget(line_frame)

        def _add_input(layout, text):
            line_edit = QLineEdit()
            line_edit.setText(text)
            line_edit.setAlignment(Qt.AlignCenter)
            line_edit.setStyleSheet("""
                QLineEdit {
                    border: none;
                    border-bottom: 2px dashed black;
                    padding-bottom: 4px;
                    background-color: transparent;
                    font-size: 14px;
                }
                """
            )
            layout.addWidget(line_edit)

        customer_layout = QVBoxLayout()
        customer_warper = QHBoxLayout()
        left_section = QVBoxLayout()
        right_section = QVBoxLayout()

        for attr in CustomerAttribute:
            _add_customer_item(
                left_section,
                f"{attr.value}:",
                QFont("Arial", InvoiceFontSize.NORMAL.value, QFont.Bold),
            )
            _add_input(right_section, "")
        customer_warper.addLayout(left_section)
        customer_warper.addLayout(right_section)

        _add_line(customer_layout)
        customer_layout.addLayout(customer_warper)
        _add_line(customer_layout)
        self.visualize_layout.addLayout(customer_layout)

    def _build_invoice_layout(self):

        def format_money(value):
            return f"{value:,.0f}"

        # ===== TOP LINE =====
        top_line = QFrame()
        top_line.setFrameShape(QFrame.HLine)
        top_line.setStyleSheet("background-color: black;")
        top_line.setFixedHeight(3)

        # ===== TABLE GRID =====
        grid = QGridLayout()
        grid.setHorizontalSpacing(30)
        grid.setVerticalSpacing(5)

        headers = ["STT", "Tên mặt hàng", "Đơn vị tính",
                "Số lượng", "Đơn giá", "Thành tiền"]

        # Header Row
        for col, text in enumerate(headers):
            label = QLabel(text)
            label.setFont(QFont("Arial", InvoiceFontSize.NORMAL.value, QFont.Bold))
            if col >= 3:
                label.setAlignment(Qt.AlignRight)
            grid.addWidget(label, 0, col)

        total = 0

        # Data Rows
        for row, item in enumerate(items, start=1):
            amount = item["qty"] * item["price"]
            total += amount

            values = [
                str(row),
                item["name"],
                item["unit"],
                str(item["qty"]),
                format_money(item["price"]),
                format_money(amount)
            ]

            for col, value in enumerate(values):
                label = QLabel(value)
                label.setFont(QFont("Arial", InvoiceFontSize.NORMAL.value))
                if col >= 3:
                    label.setAlignment(Qt.AlignRight)
                grid.addWidget(label, row, col)

        # ===== BOTTOM LINE =====
        bottom_line = QFrame()
        bottom_line.setFrameShape(QFrame.HLine)
        bottom_line.setStyleSheet("background-color: black;")
        bottom_line.setFixedHeight(3)

        # ===== TOTAL SECTION =====
        total_layout = QGridLayout()
        total_layout.setColumnStretch(0, 5)
        total_layout.setColumnStretch(1, 1)

        lbl_total_text = QLabel("Tổng Tiền:")
        lbl_total_text.setFont(QFont("Arial", InvoiceFontSize.HEADER.value, QFont.Bold))
        lbl_total_text.setAlignment(Qt.AlignRight)

        lbl_total_value = QLabel(format_money(total))
        lbl_total_value.setFont(QFont("Arial", InvoiceFontSize.HEADER.value, QFont.Bold))
        lbl_total_value.setAlignment(Qt.AlignRight)

        total_layout.addWidget(lbl_total_text, 0, 0)
        total_layout.addWidget(lbl_total_value, 0, 1)

        container = QWidget()
        invoice_layout = QVBoxLayout()
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(5)
        main_layout.addWidget(top_line)
        main_layout.addLayout(grid)
        main_layout.addWidget(bottom_line)
        main_layout.addLayout(total_layout)
        invoice_layout.addWidget(container)

        self.visualize_layout.addLayout(invoice_layout)

    def _build_signature_layout(self):

        # ===== CUSTOMER BLOCK =====
        customer_layout = QVBoxLayout()
        lbl_customer = QLabel("Đơn vị mua hàng")
        lbl_customer.setFont(QFont("Arial", InvoiceFontSize.NORMAL.value, QFont.Bold))
        lbl_customer.setAlignment(Qt.AlignCenter)
        lbl_customer_sign = QLabel("(Ký và ghi rõ họ tên)")
        lbl_customer_sign.setFont(QFont("Arial", InvoiceFontSize.NORMAL.value))
        lbl_customer_sign.setAlignment(Qt.AlignCenter)

        customer_layout.addWidget(lbl_customer)
        customer_layout.addWidget(lbl_customer_sign)
        customer_layout.addStretch()

        # ===== RECEIVED BLOCK =====
        recelved_layout = QVBoxLayout()
        lbl_received = QLabel("ĐÃ NHẬN ĐỦ TIỀN")
        lbl_received.setFont(QFont("Arial", InvoiceFontSize.NORMAL.value, QFont.Bold))
        lbl_received.setAlignment(Qt.AlignCenter)
        recelved_layout.addWidget(lbl_received)
        recelved_layout.addStretch()

        # ===== SHOP BLOCK =====
        shop_layout = QVBoxLayout()
        date_label = QLabel("Ngày ... tháng ... năm ...")
        date_label.setFont(QFont("Arial", InvoiceFontSize.NORMAL.value))
        date_label.setAlignment(Qt.AlignCenter)
        lbl_shop = QLabel("Đơn vị bán hàng")
        lbl_shop.setFont(QFont("Arial", InvoiceFontSize.NORMAL.value, QFont.Bold))
        lbl_shop.setAlignment(Qt.AlignCenter)

        sign_path = expand_env_vars_in_path(self.shop_config["sign_img"])
        if os.path.isfile(sign_path):
            sign_img = QPixmap(sign_path)
            sign_label = QLabel()
            sign_label.setPixmap(sign_img.scaled(150, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            sign_label.setAlignment(Qt.AlignCenter)

        lbl_shop_owner = QLabel(self.shop_config["shop_owner"])
        lbl_shop_owner.setFont(QFont("Arial", InvoiceFontSize.NORMAL.value))
        lbl_shop_owner.setAlignment(Qt.AlignCenter)

        shop_layout.addWidget(date_label)
        shop_layout.addWidget(lbl_shop)
        shop_layout.addWidget(sign_label)
        shop_layout.addWidget(lbl_shop_owner)
        shop_layout.addStretch()

        signature_layout = QHBoxLayout()
        signature_layout.addLayout(customer_layout)
        signature_layout.addStretch()
        signature_layout.addLayout(recelved_layout)
        signature_layout.addStretch()
        signature_layout.addLayout(shop_layout)
        self.visualize_layout.addLayout(signature_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = InvoiceVisualize()
    widget.show()
    sys.exit(app.exec_())
