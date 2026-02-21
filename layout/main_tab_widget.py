""" Main Layout Module """


import qtawesome as qta
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QTabWidget

from common.custom_widget import VerticalTabBar
from common.constants import TabAttribute
from common.styling import Style
from layout.sales_mngr.sale_management_widget import SalesManagementWidget


class MainTabWidget(QTabWidget, Style): # pylint:disable=R0903
    """ Main Tab Widget class """
    def __init__(self, context):
        super().__init__()

        self.sales_management_tab = SalesManagementWidget(context)

        self.__init_ui()

    def __init_ui(self):
        self.set_style(self)
        self.setTabPosition(QTabWidget.TabPosition.West)
        self.setTabBar(VerticalTabBar())

        self.setIconSize(QSize(32, 32))

        sale_icon = qta.icon("ri.shopping-cart-line", color="#132440")
        index = self.addTab(self.sales_management_tab, sale_icon, "")
        self.tabBar().setTabToolTip(index, TabAttribute.SALES_MANAGEMENT.value)
