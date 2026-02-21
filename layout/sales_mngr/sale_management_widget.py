""" Sales Management Widget Module """


from PyQt5.QtWidgets import QVBoxLayout, QWidget

from layout.data_collectors import DataCollectors
from layout.sales_mngr.sales_events import SalesEvents
from layout.sales_mngr.customer_layout.customer_layout import CustomerLayout
from layout.sales_mngr.bottom_layout.bottom_layout import BottomLayout
from layout.sales_mngr.middle_layout.middle_layout import MiddleLayout
from common.app_context import AppContext
from common.styling import Style


class SalesManagementWidget(QWidget, Style): # pylint:disable=R0903
    """ Sales Management widget class """
    def __init__(self, context):
        super().__init__()
        self.context: AppContext = context

        self.data_collectors = DataCollectors(self)
        self.events = SalesEvents(parent_view=self)
        self.customer_layout = CustomerLayout(self)
        self.middle_layout = MiddleLayout(self)
        self.bottom_layout = BottomLayout()

        self.__init_ui()
        self.__connect_signals()

    def __init_ui(self):
        self.sale_management_layout = QVBoxLayout()
        self.sale_management_layout.addWidget(self.customer_layout.frame)
        self.sale_management_layout.addLayout(self.middle_layout)
        self.sale_management_layout.addLayout(self.bottom_layout)
        self.setLayout(self.sale_management_layout)

    def __connect_signals(self):
        self.customer_layout.clear.clicked.connect(self.events.on_clear_customer_clicked)
        self.middle_layout.product_layout.add_button.clicked.connect(self.events.on_add_product_clicked)
        self.middle_layout.product_layout.clear_button.clicked.connect(self.events.on_clear_product_clicked)
        self.middle_layout.table_layout.table_widget.doubleClicked.connect(self.events.on_table_clicked)
        self.bottom_layout.export_button.clicked.connect(self.events.on_export_button_clicked)

    def load_suggesion_data(self, status: str = None) -> None:   # pylint: disable=unused-argument
        """ Load suggestion data """
        customers_data = self.context.mongodb_client.get_customer_info()
        self.customer_layout.load_data_suggestion(customers_data)

        products_data = self.context.mongodb_client.get_product_info()
        self.middle_layout.product_layout.load_data_suggestion(products_data)

    def handle_resize(self, width):
        """ Handle resize event """
        self.customer_layout.on_window_resize(width)
