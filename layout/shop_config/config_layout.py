""" Shop configuration layout for the application. """

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit

from common.app_context import AppContext

class ShopConfigLayout(QWidget):
    """ Layout for shop config """
    def __init__(self, parent_view):
        super().__init__()
        self.parent_view = parent_view

        self.context: AppContext = parent_view.context
        self.shop_config = self.context.shop_config
        self.init_ui()

    def init_ui(self):
        """ Initialize the UI components """
        layout = QVBoxLayout()

        # Add shop name input
        shop_name_layout = QHBoxLayout()
        shop_name_label = QLabel("Tên cửa hàng:")
        self.shop_name_input = QLineEdit()
        shop_name_layout.addWidget(shop_name_label)
        shop_name_layout.addWidget(self.shop_name_input)
        layout.addLayout(shop_name_layout)

        # Add save button
        save_button = QPushButton("Lưu")
        save_button.clicked.connect(self.save_config)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_config(self):
        """ Save the shop config to context """
        shop_name = self.shop_name_input.text()
        # Here you would save the shop name to your context or database
        print(f"Shop name saved: {shop_name}")
