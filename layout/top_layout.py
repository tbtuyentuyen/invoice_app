""" Top Layout Module """

import qtawesome as qta

from pydotdict import DotDict
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QPushButton, QWidget, QLabel

from layout.custom_widget import CustomerInputFieldLayout, VerifyInputWidget
from tools.common import CustomerAttribute, RegexPatterns, ErrorMessage


class TopLayout(QVBoxLayout, VerifyInputWidget):
    """ Top Layout class contain customer input field """

    _customer_dict = DotDict({
        CustomerAttribute.NAME: {
            'title': f'{CustomerAttribute.NAME.value}:',
            'pattern': RegexPatterns.ONLY_LETTERS,
            'error_msg': ErrorMessage.ONLY_LETTER,
        },
        CustomerAttribute.PHONE_NUMBER: {
            'title': f'{CustomerAttribute.PHONE_NUMBER.value}:',
            'pattern': RegexPatterns.PHONE_NUMBER,
            'error_msg': ErrorMessage.INVALID_PHONE,
        },
        CustomerAttribute.COMPANY: {
            'title': f'{CustomerAttribute.COMPANY.value}:',
            'pattern': RegexPatterns.LETTERS_AND_DIGITS,
            'error_msg': ErrorMessage.ONLY_LETTER_AND_NUMBER,
        },
        CustomerAttribute.ADDRESS: {
            'title': f'{CustomerAttribute.ADDRESS.value}:',
            'pattern': RegexPatterns.LETTERS_AND_DIGITS,
            'error_msg': ErrorMessage.INVALID_SPECIAL_CHAR,
        },
        CustomerAttribute.TAX_NUMBER: {
            'title': f'{CustomerAttribute.TAX_NUMBER.value}:',
            'pattern': RegexPatterns.ONLY_DIGITS,
            'error_msg': ErrorMessage.ONLY_NUMBER,
        },
        CustomerAttribute.PAYMENT_OPTIONS: {
            'title': f'{CustomerAttribute.PAYMENT_OPTIONS.value}:',
            'pattern': RegexPatterns.ONLY_LETTERS,
            'error_msg': ErrorMessage.ONLY_LETTER,
        },
    })

    def __init__(self, parent):
        self.frame = QFrame()
        self.frame.setObjectName('top_frame')
        self.set_style(self.frame)

        super().__init__(self.frame)
        self.parent = parent
        self.expand_icon = qta.icon('mdi.expand-all')
        self.collapse_icon = qta.icon('mdi.collapse-all')

        self.customer_name_phone_layout = CustomerInputFieldLayout(
            self._customer_dict[CustomerAttribute.NAME],
            self._customer_dict[CustomerAttribute.PHONE_NUMBER]
        )

        self.customer_company_layout = CustomerInputFieldLayout(
            self._customer_dict[CustomerAttribute.COMPANY]
        )

        self.customer_address_layout = CustomerInputFieldLayout(
            self._customer_dict[CustomerAttribute.ADDRESS]
        )

        self.customer_tax_payment_layout = CustomerInputFieldLayout(
            self._customer_dict[CustomerAttribute.TAX_NUMBER],
            self._customer_dict[CustomerAttribute.PAYMENT_OPTIONS]
        )

        self.toggle = QPushButton(icon=self.collapse_icon)
        self.toggle.setCheckable(True)
        self.toggle.setToolTip("Đóng bảng thông tin người mua")
        self.toggle.toggled.connect(self.on_toggle)
        self.set_style_for_toggle_button(self.toggle)

        self.customer_label = QLabel()
        self.set_style(self.customer_label)

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.customer_label)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.toggle)

        self.__init_ui()

    def on_toggle(self, checked):
        """ on_toggle """
        if checked:
            self.customer_label.setText("Thông tin người mua hàng")
            self.toggle.setIcon(self.expand_icon)
            self.toggle.setToolTip("Mở bảng thông tin người mua")
        else:
            self.customer_label.setText("")
            self.toggle.setIcon(self.collapse_icon)
            self.toggle.setToolTip("Đóng bảng thông tin người mua")

        # show/hide the container that holds all customer input layouts
        self.customer_container.setVisible(not checked)

    def __init_ui(self):
        """ Assemble the UI: put all customer layouts into a single container widget """
        # container widget and its layout to hold the customer input layouts
        self.customer_container = QWidget()
        self.customer_container_layout = QVBoxLayout(self.customer_container)
        self.customer_container_layout.setContentsMargins(0, 0, 0, 0)
        self.customer_container_layout.setSpacing(6)

         # add the customer input layouts into the container layout
        self.customer_container_layout.addLayout(self.customer_name_phone_layout)
        self.customer_container_layout.addLayout(self.customer_company_layout)
        self.customer_container_layout.addLayout(self.customer_address_layout)
        self.customer_container_layout.addLayout(self.customer_tax_payment_layout)

        # add the container widget and the button layout to this TopLayout (which is a QVBoxLayout)
        self.addWidget(self.customer_container)
        self.addLayout(self.button_layout)

    def clear_all_data_input_field(self):
        """ Clear all data in input field """
        for item in self._customer_dict.values():
            item.input_widget.clear()

    def get_data(self):
        """ Get all data from input fields """
        data = {}
        for key, item in self._customer_dict.items():
            data[key.value] = item.input_widget.text()
        return data

    def validate_all_data(self, data: dict):
        """ Validate all data before adding to table"""
        validate_status = True
        for key, value in data.items():
            if key in [CustomerAttribute.NAME.value, CustomerAttribute.PHONE_NUMBER.value] or value:
                status = self.verify_input_logic(
                    widget_dict=self._customer_dict[CustomerAttribute(key)],
                    data=value
                )
                if not status:
                    validate_status = False
        return validate_status
