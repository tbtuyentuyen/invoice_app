""" Input Layout Module """


import re
import qtawesome as qta
from pydotdict import DotDict

from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QCompleter

from layout.styling import Style
from layout.custom_widget import QMoneyLineEdit, InputFieldLayout
from tools.utils import clear_format_money
from tools.common import TableAttribute, RegexPatterns, ErrorMessage, InputMode


class InputLayout(QVBoxLayout, Style):
    """ Input layout class """

    _input_dict = DotDict({
        TableAttribute.NAME: {
            'title': 'Tên:',
            'input_cls': QLineEdit,
            'pattern': RegexPatterns.NAME,
            'error_msg': ErrorMessage.NAME_INPUT,
        },
        TableAttribute.QUANTITY: {
            'title': 'Số lượng:',
            'input_cls': QLineEdit,
            'pattern': RegexPatterns.QUANTITY,
            'error_msg': ErrorMessage.QUANTITY_INPUT,
        },
        TableAttribute.TYPE: {
            'title': 'Loại:',
            'input_cls': QLineEdit,
            'pattern': RegexPatterns.TYPE,
            'error_msg': ErrorMessage.TYPE_INPUT,
        },
        TableAttribute.PRICE: {
            'title': 'Giá:',
            'input_cls': QMoneyLineEdit,
            'pattern': RegexPatterns.PRICE,
            'error_msg': ErrorMessage.PRICE_INPUT,
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

    def __verify_input_logic(self, key: TableAttribute, data: str):
        status = False
        input_widget = self._input_dict[key].input_widget
        error_widget = self._input_dict[key].error_widget
        pattern = self._input_dict[key].pattern.value
        error_msg = self._input_dict[key].error_msg.value

        if not data:
            # data field is empty
            error_widget.setText(ErrorMessage.NONE_INPUT.value)
            self.set_style_error_widget(error_widget, is_visible=True)
            self.set_plain_text_edit_error(input_widget)

        else:
            if re.fullmatch(pattern, data.lower()):
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
            status = self.__verify_input_logic(key=key, data=item)
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
