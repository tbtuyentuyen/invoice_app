""" Input Layout Module """


import re
import qtawesome as qta
from pydotdict import DotDict

from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLineEdit, QLabel, QHBoxLayout, QCompleter

from layout.styling import Style
from common import TableAttribute, RegexPatterns, ErrorMessage, InputMode


class InputLayout(QVBoxLayout, Style):
    """ Input layout class """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.mode = InputMode.ADD

        self.name_suggestion = []
        self.type_suggestion = []

        self.name_layout = QVBoxLayout()
        self.name_label, self.name_input, self.name_error = self.__create_input_field('Tên:', self.name_layout)
        self.name_model = self.__create_completer(self.name_input, self.name_suggestion)
        self.set_style(self.name_label)
        self.set_style(self.name_input)
        self.set_style_error_widget(self.name_error, is_visible=False)

        self.quantity_layout = QVBoxLayout()
        self.quantity_label, self.quantity_input, self.quantity_error = self.__create_input_field('Số lượng:', self.quantity_layout)
        self.set_style(self.quantity_label)
        self.set_style(self.quantity_input)
        self.set_style_error_widget(self.quantity_error, is_visible=False)

        self.type_layout = QVBoxLayout()
        self.type_label, self.type_input, self.type_error = self.__create_input_field('Loại:', self.type_layout)
        self.type_model = self.__create_completer(self.type_input, self.type_suggestion)
        self.set_style(self.type_label)
        self.set_style(self.type_input)
        self.set_style_error_widget(self.type_error, is_visible=False)

        self.price_layout = QVBoxLayout()
        self.price_label, self.price_input, self.price_error = self.__create_input_field('Giá:', self.price_layout)
        self.set_style(self.price_label)
        self.set_style(self.price_input)
        self.set_style_error_widget(self.price_error, is_visible=False)

        add_icon = qta.icon('fa5s.plus-circle', color='white')
        self.add_button = QPushButton(text='Thêm', icon=add_icon)
        self.set_style(self.add_button)

        clear_icon = qta.icon('fa5s.eraser', color='white')
        self.clear_button = QPushButton(text='Xóa', icon=clear_icon)
        self.set_style(self.clear_button)

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.clear_button)

        self.__init_ui()

        self.validation_dict = DotDict({
            TableAttribute.NAME: {
                'input_widget': self.name_input, 
                'error_widget': self.name_error,
                'pattern': RegexPatterns.NAME,
                'error_msg': ErrorMessage.NAME_INPUT,
            },
            TableAttribute.QUANTITY: {
                'input_widget': self.quantity_input, 
                'error_widget': self.quantity_error,
                'pattern': RegexPatterns.QUANTITY,
                'error_msg': ErrorMessage.QUANTITY_INPUT,
            },
            TableAttribute.TYPE: {
                'input_widget': self.type_input, 
                'error_widget': self.type_error,
                'pattern': RegexPatterns.TYPE,
                'error_msg': ErrorMessage.TYPE_INPUT,
            },
            TableAttribute.PRICE: {
                'input_widget': self.price_input, 
                'error_widget': self.price_error,
                'pattern': RegexPatterns.PRICE,
                'error_msg': ErrorMessage.PRICE_INPUT,
            }
        })

    def __init_ui(self):
        self.addLayout(self.name_layout)
        self.addLayout(self.quantity_layout)
        self.addLayout(self.type_layout)
        self.addLayout(self.price_layout)
        self.addLayout(self.button_layout)
        self.addStretch()

    def __create_input_field(self, title: str, parent: QVBoxLayout):
        input_layout = QHBoxLayout()
        title_widget, input_widget = self.__create_input_part(input_layout, title)

        error_layout = QHBoxLayout()
        error_widget = self.__create_error_part(error_layout)

        parent.addLayout(input_layout)
        parent.addLayout(error_layout) 
        return title_widget, input_widget, error_widget

    def __create_input_part(self, parent: QHBoxLayout, title: str):
        title_widget = QLabel(title)
        title_widget.setFixedSize(90, 40)
        input_widget = QLineEdit()
        input_widget.setFixedSize(360, 40)

        parent.addWidget(title_widget)
        parent.addWidget(input_widget)
        return title_widget, input_widget

    def __create_error_part(self, parent: QHBoxLayout):
        error_widget = QLabel()
        error_widget.setFixedSize(360, 30)
        self.set_style_error_widget(error_widget, is_visible=False)

        parent.addStretch(1)
        parent.addWidget(error_widget)
        return error_widget

    def __create_completer(self, input_widget: QLineEdit, suggestions: list) -> QStringListModel:
        model = QStringListModel(suggestions)
        completer = QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(0)
        input_widget.setCompleter(completer)
        return model

    def __verify_input_logic(self, key: TableAttribute, data: str):
        status = False
        input_widget = self.validation_dict[key].input_widget
        error_widget = self.validation_dict[key].error_widget
        pattern = self.validation_dict[key].pattern.value
        error_msg = self.validation_dict[key].error_msg.value

        if not data:
            # data field is empty
            error_widget.setText(ErrorMessage.NONE_INPUT.value)
            self.set_style_error_widget(error_widget, is_visible=True)
            self.set_plain_text_edit_error(input_widget)

        else:
            if re.fullmatch(pattern, data):
                # data is valid
                self.set_style(input_widget)
                self.set_style_error_widget(error_widget, is_visible=False)
                status = True

            else:
                error_widget.setText(error_msg)
                self.set_style_error_widget(error_widget, is_visible=True)
                self.set_plain_text_edit_error(input_widget)

        return status

    def clear_all_data_input_field(self):
        """ Clear all data in input field """
        self.name_input.clear()
        self.quantity_input.clear()
        self.type_input.clear()
        self.price_input.clear()

    def get_data(self):
        """ Get all data from input fields """
        data = {}
        for key, item in self.validation_dict.items():
            data[key] = item.input_widget.text()
        return data

    def validate_all_data(self, data: dict):
        """ Validate all data before adding to table"""
        validate_status = True
        for key, item in data.items():
            status = self.__verify_input_logic(key=key, data=item)
            if not status:
                validate_status = False
        return validate_status

    def set_data_to_input_field(self, data: dict) -> None:
        """ Set data to input field """
        for key, item in self.validation_dict.items():
            item.input_widget.setText(data[key])

    def set_input_mode(self, mode: InputMode):
        """ Set input mode """
        if mode == InputMode.ADD:
            add_icon = qta.icon('fa5s.plus-circle', color='white')
            self.add_button.setIcon(add_icon)
            self.add_button.setText("Thêm")
            self.add_button.clicked.disconnect()
            self.add_button.clicked.connect(self.parent.parent.events.on_add_button_clicked)

        elif mode == InputMode.EDIT:
            save_icon = qta.icon("fa5s.edit", color='white')
            self.add_button.setIcon(save_icon)
            self.add_button.setText("Cập nhật")
            self.add_button.clicked.disconnect()
            self.add_button.clicked.connect(self.parent.parent.events.on_save_button_clicked)

        else:
            raise TypeError(f"[ERROR] Invalid input mode, '{mode}'")
        
        self.mode = mode
