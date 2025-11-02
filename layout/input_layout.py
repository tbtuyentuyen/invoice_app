""" Input Layout Module """


import re
import qtawesome as qta
from dotdict import dotdict

from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QPlainTextEdit, QLabel, QHBoxLayout

from layout.styling import Style
from common import VerifyType, RegexPatterns, ErrorMessage


class InputLayout(QVBoxLayout, Style):
    """ Input layout class """
    def __init__(self):
        super().__init__()

        self.name_layout = QVBoxLayout()
        self.name_label, self.name_input, self.name_error = self.__create_input_field('Tên:', self.name_layout)
        self.set_style(self.name_label)
        self.set_style(self.name_input)
        self.set_style_error_label_invisible(self.name_error)

        self.quantity_layout = QVBoxLayout()
        self.quantity_label, self.quantity_input, self.quantity_error = self.__create_input_field('Số lượng:', self.quantity_layout)
        self.set_style(self.quantity_label)
        self.set_style(self.quantity_input)
        self.set_style_error_label_invisible(self.quantity_error)

        self.type_layout = QVBoxLayout()
        self.type_label, self.type_input, self.type_error = self.__create_input_field('Loại:', self.type_layout)
        self.set_style(self.type_label)
        self.set_style(self.type_input)
        self.set_style_error_label_invisible(self.type_error)

        self.price_layout = QVBoxLayout()
        self.price_label, self.price_input, self.price_error = self.__create_input_field('Giá:', self.price_layout)
        self.set_style(self.price_label)
        self.set_style(self.price_input)
        self.set_style_error_label_invisible(self.price_error)

        add_icon = qta.icon('fa5s.plus-circle', color='white')
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton(text='Thêm', icon=add_icon)
        self.set_style(self.add_button)

        self.button_layout.addStretch()
        self.button_layout.addWidget(self.add_button)
        self.__init_ui()

    def __init_ui(self):
        self.addLayout(self.name_layout)
        self.addLayout(self.quantity_layout)
        self.addLayout(self.type_layout)
        self.addLayout(self.price_layout)
        self.addLayout(self.button_layout)
        self.addStretch()

    def __create_input_field(self, title: str, parent: QVBoxLayout):
        input_field = QHBoxLayout()
        error_field = QHBoxLayout()

        label, text_input = self.__create_input_part(input_field, title)
        error_label = self.__create_error_part(error_field)

        parent.addLayout(input_field)
        parent.addLayout(error_field)
        return label, text_input, error_label

    def __create_input_part(self, parent: QHBoxLayout, title: str):
        label = QLabel(title)
        text_input = QPlainTextEdit()

        text_input.setFixedSize(360, 40)
        label.setFixedSize(90, 40)
        parent.addWidget(label)
        parent.addWidget(text_input)

        return label, text_input

    def __create_error_part(self, parent: QHBoxLayout):
        error_label = QLabel()

        error_label.setFixedSize(360, 30)
        error_label.setStyleSheet("color: transparent;")
        parent.addStretch(1)
        parent.addWidget(error_label)

        return error_label

    def __verify_input_logic(self, input_widget: QPlainTextEdit, error_widget: QLabel, pattern: str, error_msg: str):
        data_status = False
        data = input_widget.toPlainText()
        input_widget.blockSignals(True)

        if not data:
            error_widget.setText(ErrorMessage.NONE_INPUT)
            self.set_style_error_label_visible(error_widget)
            self.set_plain_text_edit_error(input_widget)

        elif re.fullmatch(pattern, data):
            data_status = True
            self.set_style(input_widget)
            if error_widget.isVisible():
                self.set_style_error_label_invisible(error_widget)
        else:
            error_widget.setText(error_msg)
            self.set_style_error_label_visible(error_widget)
            self.set_plain_text_edit_error(input_widget)

        input_widget.blockSignals(False)
        return data_status

    def clear_all_data_input_field(self):
        """ Clear all data in input field """
        self.name_input.clear()
        self.quantity_input.clear()
        self.type_input.clear()
        self.price_input.clear()

    def validate_all_data(self):
        """ Validate all data before adding to table"""
        data_map = {}
        validation_map = {
            VerifyType.NAME: {
                'input_widget': self.name_input, 
                'error_widget': self.name_error,
                'pattern': RegexPatterns.NAME,
                'error_msg': ErrorMessage.NAME_INPUT,
            },
            VerifyType.QUANTITY: {
                'input_widget': self.quantity_input, 
                'error_widget': self.quantity_error,
                'pattern': RegexPatterns.QUANTITY,
                'error_msg': ErrorMessage.QUANTITY_INPUT,
            },
            VerifyType.TYPE: {
                'input_widget': self.type_input, 
                'error_widget': self.type_error,
                'pattern': RegexPatterns.TYPE,
                'error_msg': ErrorMessage.TYPE_INPUT,
            },
            VerifyType.PRICE: {
                'input_widget': self.price_input, 
                'error_widget': self.price_error,
                'pattern': RegexPatterns.PRICE,
                'error_msg': ErrorMessage.PRICE_INPUT,
            }
        }

        validation_dot = dotdict(validation_map)
        for verify_type, validation_info in validation_dot.items():
            validate_result = self.__verify_input_logic(
                                        input_widget=validation_info.input_widget,
                                        error_widget=validation_info.error_widget,
                                        pattern=validation_info.pattern,
                                        error_msg=validation_info.error_msg)
            if validate_result is True:
                data_map[verify_type] = validation_info.input_widget.toPlainText()
        return data_map
