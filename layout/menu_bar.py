""" Menu bar moodule """

from PyQt5.QtWidgets import QMenuBar, QAction

class MenuBar(QMenuBar):
    """ Menu bar class """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        setting_menu = self.addMenu('Cài đặt')
        self.export_path_action = QAction("Nơi lưu hóa đơn", self)
        self.export_path_action.triggered.connect(self.parent.main_layout.events.on_set_export_path_clicked)
        setting_menu.addAction(self.export_path_action)
