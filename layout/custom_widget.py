""" Custom Widget module """


import re
from pydotdict import DotDict
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QTableWidget, QMenu, QVBoxLayout, QHBoxLayout, QLabel

from tools.utils import clear_format_money
from tools.common import ErrorMessage, TableAttribute
from layout.styling import Style


class QMoneyLineEdit(QLineEdit):
    """
    A QLineEdit subclass that formats numeric input into Vietnamese currency.

    - Automatically adds thousand separators (.)
    - Appends the suffix " VNĐ"
    - Maintains cursor position while typing
    - Rejects invalid numeric characters
    """

    prefix = " VNĐ"

    def __init__(self):
        """Initialize widget and connect formatting signals."""
        super().__init__()
        self.textChanged.connect(self.format_currency)
        self.setAlignment(Qt.AlignRight)

    def format_currency(self):
        """
        Format the line edit's content into currency format.

        Steps:
        1. Strip formatting using clear_format_money()
        2. Validate that result is numeric
        3. Insert thousand separators
        4. Append " VNĐ"
        5. Preserve cursor before the suffix
        """
        text = self.text()
        cleaned = clear_format_money(text)

        # Ensure cleaned text is digits only
        if not cleaned.isdigit():
            return

        value = int(cleaned)
        formatted = f"{value:,}".replace(",", ".") + self.prefix

        # Block signal to prevent recursion
        self.blockSignals(True)
        self.setText(formatted)
        self.blockSignals(False)

        # Position cursor right before the suffix
        cursor_pos = len(formatted) - len(self.prefix)
        self.setCursorPosition(cursor_pos)

    def get_value(self):
        """Return the numeric value as int, or None if invalid."""
        cleaned = clear_format_money(self.text())
        return int(cleaned) if cleaned.isdigit() else None

    @property
    def value(self):
        """Property exposing the parsed integer value."""
        return self.get_value()


class QCustomTableWidget(QTableWidget):
    """
    A QTableWidget that adds right-click context menu support.

    Expected parent methods:
    - highlight_edit_row(row, column)
    - delete_data_by_row(checked, row)
    - clean_table_color()
    """

    def __init__(self, parent=None):
        """Store parent for callback use."""
        super().__init__()
        self.parent = parent

    def mousePressEvent(self, event):  # pylint: disable=invalid-name
        """
        Override mouse press handler to add context menu on right-click.

        Behavior:
        - Detect right-click
        - Identify clicked row/column
        - Highlight row through parent callback
        - Show context menu with "Delete row" action
        - Execute delete action via parent method
        - Clean highlight after menu closes
        """
        super().mousePressEvent(event)
        if event.button() == Qt.RightButton:
            item = self.itemAt(event.pos())

            # Ignore if right-click is outside valid cell
            if item is None:
                return

            row = item.row()
            col = item.column()

            # Notify parent to highlight
            if hasattr(self.parent, "highlight_edit_row"):
                self.parent.highlight_edit_row(row, col)

            # Build context menu
            menu = QMenu(self)
            delete_action = menu.addAction("Xóa hàng")

            # Connect delete action
            delete_action.triggered.connect(
                lambda checked_state: self.parent.delete_data_by_row(checked_state, row)
            )

            # Show menu at cursor
            menu.exec_(self.mapToGlobal(event.pos()))

            # Clean highlight
            self.parent.clean_table_color()


class InputFieldLayout(QVBoxLayout, Style):
    """ Input Field Layout class """
    def __init__(self, input_dict: DotDict):
        super().__init__()
        label_w, label_h = 90, 40
        input_w, input_h = 360, 40
        error_w, error_h = 360, 30

        self.title_widget = QLabel(input_dict.title)
        self.title_widget.setFixedSize(label_w, label_h)
        self.set_style(self.title_widget)

        self.input_widget:QLineEdit = input_dict.input_cls()
        self.input_widget.setFixedSize(input_w, input_h)
        self.set_style(self.input_widget)
        self._connect_text_entered(
            input_dict.input_cls,
            input_dict.is_title,
            input_dict.pattern.value,
            input_dict.error_msg.value
        )

        self.error_widget = QLabel()
        self.error_widget.setFixedSize(error_w, error_h)
        self.set_style_error_widget(self.error_widget, is_visible=False)

        self.__init_ui()

        input_dict.update({
            'input_widget': self.input_widget,
            'error_widget': self.error_widget
        })

    def __init_ui(self):
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.title_widget)
        input_layout.addWidget(self.input_widget)

        error_layout = QHBoxLayout()
        error_layout.addStretch(1)
        error_layout.addWidget(self.error_widget)

        self.addLayout(input_layout)
        self.addLayout(error_layout)

    def _connect_text_entered(self, widget_cls, is_title:bool, pattern: str, error_msg: str):
        """Connect textChanged to an uppercase function with recursion guard."""
        def on_text_changed(text):
            # ---- 1. Title Case formatting ----
            if is_title:
                if text:
                    formatted = text.title()
                else:
                    formatted = text

                if formatted != text:
                    cursor_pos = self.input_widget.cursorPosition()
                    self.input_widget.blockSignals(True)
                    self.input_widget.setText(formatted)
                    self.input_widget.setCursorPosition(cursor_pos)
                    self.input_widget.blockSignals(False)

            # ---- 2. Regex validation ----
            if widget_cls == QMoneyLineEdit:
                text = clear_format_money(text)
            if re.fullmatch(pattern, text.lower()):
                # Valid or empty → hide error
                self.set_style(self.input_widget) # Border normal
                self.set_style_error_widget(self.error_widget, is_visible=False)
            else:
                # Invalid → show error
                self.error_widget.setText(error_msg)
                self.set_plain_text_edit_error(self.input_widget) # Border red
                self.set_style_error_widget(self.error_widget, is_visible=True)

        self.input_widget.textChanged.connect(on_text_changed)

class CustomerInputFieldLayout(QHBoxLayout, Style):
    """Customer Input Field Layout class"""

    def __init__(self, left_attr: DotDict, right_attr: DotDict = None):
        super().__init__()

        self.left_field = self._build_field(left_attr)
        self._add_field_to_layout(self.left_field)
        left_attr.update({
            'input_widget': self.left_field.input_widget,
            'error_widget': self.left_field.error_widget
        })

        # If row have 2 column
        self.right_field = None
        if right_attr:
            self.addStretch(1)
            self.right_field = self._build_field(right_attr)
            self._add_field_to_layout(self.right_field)
            right_attr.update({
                'input_widget': self.right_field.input_widget,
                'error_widget': self.right_field.error_widget
            })

        self.addStretch(1)

    def _build_field(self, info_dict: DotDict) -> dict:
        title_widget = QLabel(info_dict.title)
        self.set_style_customer_label_widget(title_widget)

        input_widget = QLineEdit()
        self.set_style_customer_input_widget(input_widget)

        error_widget = QLabel()
        self.set_style_error_widget(error_widget, is_visible=False)

        return DotDict({
            'title_widget': title_widget,
            'input_widget': input_widget,
            'error_widget': error_widget
        })

    def _add_field_to_layout(self, widgets: DotDict):
        input_layout = QHBoxLayout()
        input_layout.addWidget(widgets.title_widget)
        input_layout.addWidget(widgets.input_widget)

        error_layout = QHBoxLayout()
        error_layout.addStretch(2)
        error_layout.addWidget(widgets.error_widget)

        combo = QVBoxLayout()
        combo.addLayout(input_layout)
        combo.addLayout(error_layout)

        self.addLayout(combo)

class VerifyInputWidget(Style):
    """ Verify Input Widget class """
    def verify_input_logic(self, widget_dict: DotDict, data: str):
        """ Verify input logic function """
        status = False
        input_widget = widget_dict.input_widget
        error_widget = widget_dict.error_widget
        pattern = widget_dict.pattern.value
        error_msg = widget_dict.error_msg.value

        if not data:
            # data field is empty
            error_widget.setText(ErrorMessage.EMPTY_INPUT.value)
            self.set_style_error_widget(error_widget, is_visible=True)
            self.set_plain_text_edit_error(input_widget)

        else:
            if re.fullmatch(pattern, data.lower()):
                # data is valid
                if widget_dict.title.replace(':', '') in TableAttribute.list():
                    self.set_style(input_widget)
                else:
                    self.set_style_customer_input_widget(input_widget)
                self.set_style_error_widget(error_widget, is_visible=False)
                status = True

            else:
                error_widget.setText(error_msg)
                self.set_style_error_widget(error_widget, is_visible=True)
                self.set_plain_text_edit_error(input_widget)

        return status
