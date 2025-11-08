""" Bottom Layout Module """


import qtawesome as qta

from PyQt5.QtWidgets import QHBoxLayout, QPushButton

from layout.styling import Style


class BottomLayout(QHBoxLayout, Style):
    """ Bottom layout class """
    def __init__(self):
        super().__init__()

        save_icon = qta.icon('fa5s.file-export', color='white')
        self.save_button = QPushButton(text='Xuất hóa đơn', icon=save_icon)
        self.set_style(self.save_button)

        self.__init_ui()

    def __init_ui(self):
        self.addStretch()
        self.addWidget(self.save_button)
