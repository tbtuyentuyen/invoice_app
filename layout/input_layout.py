""" Input Layout Module """


import os

import qtawesome as qta
from pydotdict import DotDict

from PyQt5.QtCore import QStringListModel, Qt, QTimer
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QCompleter

from layout.styling import Style
from layout.custom_widget import QMoneyLineEdit, InputFieldLayout, VerifyInputWidget
from tools.utils import clear_format_money, load_pickle, save_pickle
from tools.common import TableAttribute, RegexPatterns, ErrorMessage, InputMode


CONFIG_DIR = os.environ['CONFIG_DIR']
PRODUCT_DATA_PATH = os.path.join(CONFIG_DIR, "recommend/product_data.pkl")

class InputLayout(QVBoxLayout, VerifyInputWidget, Style):
    """ Input layout class """
    
    _input_dict = DotDict({
        TableAttribute.NAME: {
            'title': f'{TableAttribute.NAME.value}:',
            'input_cls': QLineEdit,
            'pattern': RegexPatterns.LETTERS_AND_DIGITS,
            'error_msg': ErrorMessage.ONLY_LETTER_AND_NUMBER,
            'is_title': True
        },
        TableAttribute.QUANTITY: {
            'title': f'{TableAttribute.QUANTITY.value}:',
            'input_cls': QLineEdit,
            'pattern': RegexPatterns.ONLY_DIGITS,
            'error_msg': ErrorMessage.ONLY_NUMBER,
            'is_title': False
        },
        TableAttribute.TYPE: {
            'title': f'{TableAttribute.TYPE.value}:',
            'input_cls': QLineEdit,
            'pattern': RegexPatterns.LETTERS_AND_DIGITS,
            'error_msg': ErrorMessage.ONLY_LETTER_AND_NUMBER,
            'is_title': True
        },
        TableAttribute.PRICE: {
            'title': f'{TableAttribute.PRICE.value}:',
            'input_cls': QMoneyLineEdit,
            'pattern': RegexPatterns.ONLY_DIGITS,
            'error_msg': ErrorMessage.ONLY_NUMBER,
            'is_title': False
        }
    })

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.mode = InputMode.ADD

        self.name_suggestion = None
        self.type_suggestion = None

        self.name_layout = InputFieldLayout(self._input_dict[TableAttribute.NAME])
        self.name_model, self.name_compliter = self.create_completer()
        self.name_layout.input_widget.setCompleter(self.name_compliter)
        self.name_compliter.activated.connect(self.fill_fields)

        self.quatity_layout = InputFieldLayout(self._input_dict[TableAttribute.QUANTITY])

        self.type_layout = InputFieldLayout(self._input_dict[TableAttribute.TYPE])
        self.type_model, type_compliter = self.create_completer()
        self.type_layout.input_widget.setCompleter(type_compliter)
        

        self.price_layout = InputFieldLayout(self._input_dict[TableAttribute.PRICE])

        add_icon = qta.icon('fa5s.plus-circle', color='white')
        self.add_button = QPushButton(text='Thêm', icon=add_icon)
        self.add_button.setObjectName('common_button')
        self.set_style(self.add_button)

        clear_icon = qta.icon('fa5s.eraser', color='white')
        self.clear_button = QPushButton(text='Xóa', icon=clear_icon)
        self.clear_button.setObjectName('common_button')
        self.set_style(self.clear_button)

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.clear_button)

        self.__init_ui()
        self.load_data_suggestion()
        self.set_data_suggestion()

    def __init_ui(self):
        self.addLayout(self.name_layout)
        self.addLayout(self.quatity_layout)
        self.addLayout(self.type_layout)
        self.addLayout(self.price_layout)
        self.addLayout(self.button_layout)
        self.addStretch()

    def create_completer(self) -> tuple[QStringListModel, QCompleter]:
        """ Create completer for customer name and phone number """
        model = QStringListModel()
        completer = QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        return model, completer

    def clear_all_data_input_field(self):
        """ Clear all data in input field """
        for item in self._input_dict.values():
            item.input_widget.clear()
            item.error_widget.setObjectName('invisible_error_label')
            self.set_style(item.error_widget)
            self.set_style(item.input_widget)

    def get_data(self):
        """ Get all data from input fields """
        data = {}
        for key, item in self._input_dict.items():
            value = item.input_widget.text()
            if key == TableAttribute.PRICE:
                value = clear_format_money(value)
            data[key] = value
        return data

    def validate_all_data(self, data: dict):
        """ Validate all data before adding to table"""
        validate_status = True
        for key, item in data.items():
            status = self.verify_input_logic(widget_dict=self._input_dict[key], data=item)
            if not status:
                validate_status = False
        return validate_status

    def set_data_to_input_field(self, data: dict) -> None:
        """ Set data to input field """
        for key, item in self._input_dict.items():
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

    def load_data_suggestion(self) -> None:
        """ Load name and type suggestion """
        if os.path.isfile(PRODUCT_DATA_PATH):
            data = load_pickle(PRODUCT_DATA_PATH)
            self.name_suggestion = data[TableAttribute.NAME]
            self.type_suggestion = data[TableAttribute.TYPE]
        else:
            self.name_suggestion = []
            self.type_suggestion = []

    def save_data_suggestion(self) -> None:
        """ Save name and type suggestion """
        data = {
            TableAttribute.NAME: self.name_suggestion,
            TableAttribute.TYPE: self.type_suggestion
        }
        os.makedirs(os.path.dirname(PRODUCT_DATA_PATH), exist_ok=True)
        save_pickle(data, PRODUCT_DATA_PATH)

    def set_data_suggestion(self) -> None:
        """ Set name and type suggestion """
        combined_list = [f"{name_str} - {price_str}"
                         for name_str, price_str, _ in self.name_suggestion]
        self.name_model.setStringList(combined_list)
        self.type_model.setStringList(self.type_suggestion)

    def update_data_suggestion(self, data: dict) -> None:
        """ Update name and type suggestion """
        name_str = data[TableAttribute.NAME]
        type_str = data[TableAttribute.TYPE]
        price_str = data[TableAttribute.PRICE]
        combine_data = (name_str, price_str, type_str)

        if combine_data not in self.name_suggestion:
            self.name_suggestion.append(combine_data)

        if type_str and type_str not in self.type_suggestion:
            self.type_suggestion.append(type_str)

        self.set_data_suggestion()

    def fill_fields(self, text: str) -> None:
        """ Fill fields when select suggestion """
        name_part = text.split(" - ")[0]
        for name_str, price_str, type_str in self.name_suggestion:
            if name_part == name_str:
                QTimer.singleShot(0, lambda: self.name_layout.input_widget.setText(name_str))
                QTimer.singleShot(0, lambda: self.price_layout.input_widget.setText(price_str))
                QTimer.singleShot(0, lambda: self.type_layout.input_widget.setText(type_str))
                break
