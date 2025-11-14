""" Custom Widget module """


from pydotdict import DotDict
from PyQt5.QtWidgets import QLineEdit, QTableWidget, QMenu, QVBoxLayout, QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

from tools.utils import clear_format_money
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

        self.input_widget = input_dict.input_cls()
        self.input_widget.setFixedSize(input_w, input_h)
        self.set_style(self.input_widget)

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
