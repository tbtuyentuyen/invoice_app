""" Input Layout Module """


import qtawesome as qta
from pydotdict import DotDict

from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QCompleter

from layout.custom_widget import QMoneyLineEdit, InputFieldLayout, VerifyInputWidget
from tools.utils import clear_format_money
from tools.common import TableAttribute, RegexPatterns, ErrorMessage, InputMode


class InputLayout(QVBoxLayout, VerifyInputWidget):
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

        self.name_suggestion = []
        self.type_suggestion = []

        self.name_layout = InputFieldLayout(self._input_dict[TableAttribute.NAME])
        self.name_model = self.__create_completer(
            self.name_layout.input_widget, self.name_suggestion
        )

        self.quatity_layout = InputFieldLayout(self._input_dict[TableAttribute.QUANTITY])

        self.type_layout = InputFieldLayout(self._input_dict[TableAttribute.TYPE])
        self.type_model = self.__create_completer(
            self.type_layout.input_widget, self.type_suggestion
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

    def __init_ui(self):
        self.addLayout(self.name_layout)
        self.addLayout(self.quatity_layout)
        self.addLayout(self.type_layout)
        self.addLayout(self.price_layout)
        self.addLayout(self.button_layout)
        self.addStretch()

    def __create_completer(self, input_widget: QLineEdit, suggestions: list) -> QStringListModel:
        model = QStringListModel(suggestions)
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
