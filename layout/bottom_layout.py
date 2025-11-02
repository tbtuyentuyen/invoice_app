""" Bottom Layout Module """


import qtawesome as qta

from PyQt5.QtWidgets import QHBoxLayout, QPushButton

from layout.styling import Style


class BottomLayout(QHBoxLayout, Style):
    """ Bottom layout class """
    def __init__(self):
        super().__init__()

        save_icon = qta.icon('fa5s.save', color='white')
        self.save_button = QPushButton(text='Lưu', icon=save_icon)
        self.set_style(self.save_button)

        clear_icon = qta.icon('ri.brush-3-fill', color='white')
        self.clear_button = QPushButton(text='Xóa toàn bộ', icon=clear_icon)
        self.set_style(self.clear_button)

        self.__init_ui()

    def __init_ui(self):
        self.addStretch()
        self.addWidget(self.clear_button)
        self.addWidget(self.save_button)
