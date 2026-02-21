""" Top Layout Module """

import qtawesome as qta

from pydotdict import DotDict
from PyQt5.QtCore import QStringListModel, QTimer, Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QPushButton, QWidget, QLabel, QCompleter

from common.custom_widget import CustomerInputFieldLayout, VerifyInputWidget
from common.constants import CustomerAttribute, RegexPatterns, ErrorMessage


class CustomerLayout(QVBoxLayout, VerifyInputWidget):
    """ Customer Layout class contain customer input field """
    DUAL_SCALE = 0.25
    INVIDUAL_SCALE = 0.75

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
        self.parent_view = parent
        self.expand_icon = qta.icon('mdi.expand-all')
        self.collapse_icon = qta.icon('mdi.collapse-all')
        self.clear_icon = qta.icon('mdi6.broom', color='white')

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

        self.user_suggestion = {}
        self.user_model, self.completer = self.create_completer()
        self.customer_name_phone_layout.left_field.input_widget.setCompleter(self.completer)
        self.customer_name_phone_layout.right_field.input_widget.setCompleter(self.completer)
        self.completer.activated.connect(self.fill_fields)

        self.toggle = QPushButton(icon=self.collapse_icon)
        self.toggle.setObjectName('expand_toggle')
        self.toggle.setCheckable(True)
        self.toggle.setToolTip("Đóng bảng thông tin người mua")
        self.toggle.toggled.connect(self.on_toggle)
        self.set_style(self.toggle)

        self.clear = QPushButton(icon=self.clear_icon)
        self.clear.setToolTip("Xóa tất cả thông tin người mua")
        self.clear.setObjectName('common_button')
        self.set_style(self.clear)

        self.customer_label = QLabel()
        self.customer_label.setObjectName('title_label')
        self.set_style(self.customer_label)

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.customer_label)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.clear)
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
        self.clear.setVisible(not checked)

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

        # add the container widget and the button layout to this CustomerLayout (which is a QVBoxLayout)
        self.addWidget(self.customer_container)
        self.addLayout(self.button_layout)

    def clear_all_data_input_field(self):
        """ Clear all data in input field """
        for item in self._customer_dict.values():
            item.input_widget.clear()
            item.input_widget.setObjectName('customer_input')
            item.error_widget.setObjectName('invisible_error_label')
            self.set_style(item.error_widget)
            self.set_style(item.input_widget)

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

    def on_window_resize(self, window_w: int):
        """ resize event"""
        for layout in ['customer_name_phone_layout', 'customer_company_layout',
                       'customer_address_layout', 'customer_tax_payment_layout']:
            product_layout = getattr(self, layout)
            if product_layout.right_field:
                product_layout.left_field.input_widget.setFixedWidth(int(window_w * self.DUAL_SCALE))
                product_layout.left_field.error_widget.setFixedWidth(int(window_w * self.DUAL_SCALE))
                product_layout.right_field.input_widget.setFixedWidth(int(window_w * self.DUAL_SCALE))
                product_layout.right_field.error_widget.setFixedWidth(int(window_w * self.DUAL_SCALE))
            else:
                product_layout.left_field.input_widget.setFixedWidth(int(window_w * self.INVIDUAL_SCALE))
                product_layout.left_field.error_widget.setFixedWidth(int(window_w * self.INVIDUAL_SCALE))

    def create_completer(self) -> tuple[QStringListModel, QCompleter]:
        """ Create completer for customer name and phone number """
        model = QStringListModel()
        completer = QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        return model, completer

    def load_data_suggestion(self, data: list) -> None:
        """ Load name and type suggestion """
        for customer in data:
            self.user_suggestion[customer['_id']] = customer
        self.set_data_suggestion()

    def set_data_suggestion(self) -> None:
        """ Set name and type suggestion """
        combined_list = [f"{data[CustomerAttribute.NAME.value]} - {phone}"
                         for phone, data in self.user_suggestion.items()]
        self.user_model.setStringList(combined_list)

    def fill_fields(self, text):
        """Fill name and phone fields when selecting from completer"""
        if " - " in text:
            _, phone = text.split(" - ", 1)
            customer_data = self.user_suggestion[phone]
            QTimer.singleShot(0, lambda: self.customer_name_phone_layout.left_field.input_widget.setText(
                customer_data[CustomerAttribute.NAME.value]
            ))
            QTimer.singleShot(0, lambda: self.customer_name_phone_layout.right_field.input_widget.setText(
                customer_data[CustomerAttribute.PHONE_NUMBER.value]
            ))
            QTimer.singleShot(0, lambda: self.customer_company_layout.left_field.input_widget.setText(
                customer_data[CustomerAttribute.COMPANY.value]
            ))
            QTimer.singleShot(0, lambda: self.customer_address_layout.left_field.input_widget.setText(
                customer_data[CustomerAttribute.ADDRESS.value]
            ))
            QTimer.singleShot(0, lambda: self.customer_tax_payment_layout.left_field.input_widget.setText(
                customer_data[CustomerAttribute.TAX_NUMBER.value]
            ))
