""" Input Layout Module """


import os

import qtawesome as qta
from pydotdict import DotDict

from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QCompleter

from layout.custom_widget import QMoneyLineEdit, InputFieldLayout, VerifyInputWidget
from tools.utils import clear_format_money, load_pickle, save_pickle
from tools.common import TableAttribute, RegexPatterns, ErrorMessage, InputMode


INVOICE_APP_PATH = os.environ['INVOICE_APP_PATH']

class InputLayout(QVBoxLayout, VerifyInputWidget):
    """ Input layout class """
    RECOMMEND_DATA_PATH = os.path.join(INVOICE_APP_PATH, "data/recommend/product_data.pkl")
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

        self.name_suggestion = []
        self.type_suggestion = []

        self.name_layout = InputFieldLayout(self._input_dict[TableAttribute.NAME])
        self.name_model = self.__create_completer(
            self.name_layout.input_widget
        )

        self.quatity_layout = InputFieldLayout(self._input_dict[TableAttribute.QUANTITY])

        self.type_layout = InputFieldLayout(self._input_dict[TableAttribute.TYPE])
        self.type_model = self.__create_completer(
            self.type_layout.input_widget
        )

        self.price_layout = InputFieldLayout(self._input_dict[TableAttribute.PRICE])

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
        self.load_data_suggestion()
        self.set_data_suggestion()

    def __init_ui(self):
        self.addLayout(self.name_layout)
        self.addLayout(self.quatity_layout)
        self.addLayout(self.type_layout)
        self.addLayout(self.price_layout)
        self.addLayout(self.button_layout)
        self.addStretch()

    def __create_completer(self, input_widget: QLineEdit) -> QStringListModel:
        model = QStringListModel()
        completer = QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(0)
        input_widget.setCompleter(completer)
        return model

    def clear_all_data_input_field(self):
        """ Clear all data in input field """
        for item in self._input_dict.values():
            item.input_widget.clear()

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
        if os.path.isfile(self.RECOMMEND_DATA_PATH):
            data = load_pickle(self.RECOMMEND_DATA_PATH)
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
        os.makedirs(os.path.dirname(self.RECOMMEND_DATA_PATH), exist_ok=True)
        save_pickle(data, self.RECOMMEND_DATA_PATH)

    def set_data_suggestion(self) -> None:
        """ Set name and type suggestion """
        self.name_model.setStringList(self.name_suggestion)
        self.type_model.setStringList(self.type_suggestion)

    def update_data_suggestion(self, data: dict) -> None:
        """ Update name and type suggestion """
        name_str = data[TableAttribute.NAME]
        type_str = data[TableAttribute.TYPE]

        if name_str and name_str not in self.name_suggestion:
            self.name_suggestion.append(name_str)

        if type_str and type_str not in self.type_suggestion:
            self.type_suggestion.append(type_str)

        self.set_data_suggestion()
