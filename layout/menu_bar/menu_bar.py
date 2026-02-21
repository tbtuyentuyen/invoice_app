""" Menu bar moodule """

from PyQt5.QtWidgets import QMenuBar, QAction

from common.app_context import AppContext

class MenuBar(QMenuBar):
    """ Menu bar class """
    def __init__(self, parent_view):
        super().__init__()
        self.parent_view = parent_view
        self.context: AppContext = parent_view.context
        setting_menu = self.addMenu('Cài đặt')

        self.export_path_action = QAction("Nơi lưu hóa đơn", self)
        self.export_path_action.triggered.connect(self.parent_view.events.on_set_export_path_clicked)
        setting_menu.addAction(self.export_path_action)

        self.check_db_connection = QAction("Kiểm tra kết nối database", self)
        self.check_db_connection.triggered.connect(self.context.mongodb_client.start)
        setting_menu.addAction(self.check_db_connection)
