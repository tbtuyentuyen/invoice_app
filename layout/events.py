""" Events Module """


from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QFileDialog

from tools.process_helper import stop_broker
from tools.utils import expand_env_vars_in_path
from common.constants import MessageBoxType
from common.custom_widget import MessageBoxWidget


class Events():   # pylint:disable=R0903
    """ Events class to handle application events such as closing the app """
    def __init__(self, parent_view):
        self.parent_view = parent_view
        self.context = parent_view.context

    def handle_close(self, event: QCloseEvent):
        """ Handle the close event of the application with a confirmation dialog """
        close_box = MessageBoxWidget(
            MessageBoxType.QUESTION,
            "Xác nhận đóng ứng dụng",
            "Dữ liệu của phiên làm việc hiện tại sẽ bị xóa.\nNhấn 'Có' nếu bạn muốn đóng ứng dụng."
        )
        close_box.exec_()

        if close_box.clickedButton() == close_box.button_accept:
            stop_broker()
            event.accept()
        else:
            event.ignore()

    def on_set_export_path_clicked(self):
        """ Event clicked on set export path """
        folder_path = QFileDialog.getExistingDirectory(
            None, "Select Folder", expand_env_vars_in_path(self.context.config.export_folder)
        )

        if folder_path:
            self.context.config.export_folder = folder_path
