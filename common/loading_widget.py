"""
Loading widget that simulates application startup and checks MongoDB connection
"""


import time
import threading

from PyQt5.QtWidgets import QFrame, QWidget, QVBoxLayout, QProgressBar, QLabel, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt, QRectF, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor

from common.custom_widget import MessageBoxWidget
from common.constants import MessageBoxType
from common.styling import Style
from tools.mongodb_client import MongoDBClient
from tools.process_helper import start_broker

class CircularLoading(QWidget):
    """ Circular loading animation widget """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(80, 80)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(15)

    def rotate(self):
        """ Rotate the loading arc and trigger repaint """
        self.angle = (self.angle + 8) % 360
        self.update()

    def paintEvent(self, event):
        """ Paint the circular loading animation """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(10, 10, 60, 60)

        painter.setPen(QPen(QColor(255, 255, 255, 20), 5))
        painter.drawEllipse(rect)

        painter.setPen(QPen(QColor("#48B3AF"), 5, Qt.SolidLine, Qt.RoundCap))
        painter.drawArc(rect, -self.angle * 16, 80 * 16)

class LoadingWidget(QWidget, Style):
    """ Loading widget that simulates application startup and checks MongoDB connection """
    progress_update = pyqtSignal(int)
    percent_update = pyqtSignal(str)
    finished = pyqtSignal()
    failed = pyqtSignal()

    def __init__(self, mongodb_client: MongoDBClient):
        super().__init__()
        self.mongodb_client = mongodb_client
        self.init_ui()

    def init_ui(self):
        """ initialize the UI components"""
        self.setWindowTitle('PyQt5 Professional Loading Bar')
        self.setFixedSize(800, 300)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.98)

        glass_effect = QFrame(self)
        glass_effect.setObjectName("loading_frame")
        self.set_style(glass_effect)
        glass_effect.setGeometry(0, 0, 800, 300)
        layout = QVBoxLayout(glass_effect)

        self.loading_circle = CircularLoading(self)
        layout.addWidget(self.loading_circle, 0, Qt.AlignCenter)
        layout.addSpacing(20)

        h_layout = QHBoxLayout()
        self.label_desc = QLabel("Đang mở ứng dụng...", self)
        self.label_desc.setObjectName("loading_label")
        self.set_style(self.label_desc)
        self.label_percent = QLabel("0%", self)
        self.label_percent.setObjectName("loading_label")
        self.set_style(self.label_percent)

        h_layout.addWidget(self.label_desc)
        h_layout.addStretch()
        h_layout.addWidget(self.label_percent)

        # ProgressBar
        self.pbar = QProgressBar(self)
        self.pbar.setTextVisible(False)
        self.pbar.setMinimumHeight(15)
        self.set_style(self.pbar)

        layout.addWidget(self.pbar)
        layout.addLayout(h_layout)
        layout.addSpacing(20)
        layout.setContentsMargins(60, 40, 60, 40)
        self.setLayout(layout)

    def on_connect_failed(self):
        """ On connection failure, show error message and close the loading widget """
        warning_box = MessageBoxWidget(
            MessageBoxType.ERROR,
            "Mở ứng dụng thất bại",
            "Không thể kết nối đến MongoDB. Vui lòng kiểm tra lại kết nối và khởi động lại ứng dụng."
        )
        warning_box.exec_()
        self.close()

    def run(self):
        """ Thread function to simulate loading and check MongoDB connection """
        start_broker()
        wait_time = 5
        tick_time = 0.1
        start_time = time.monotonic()
        while time.monotonic() - start_time < wait_time:
            time.sleep(tick_time)
            elapsed = time.monotonic() - start_time
            percent = int((elapsed / wait_time) * 100)
            self.percent_update.emit(str(percent) + '%')
            self.progress_update.emit(percent)
        sts = self.mongodb_client.check_connection()
        if not sts:
            self.failed.emit()
        else:
            self.finished.emit()

    def start_loading(self, show_callback):
        """ Start the loading process and show the widget """
        self.show()
        self.percent_update.connect(self.label_percent.setText)
        self.progress_update.connect(self.pbar.setValue)
        self.finished.connect(show_callback)
        self.finished.connect(self.close)
        self.failed.connect(self.on_connect_failed)
        loading_thread = threading.Thread(target=self.run, name="LoadingThread", daemon=True)
        loading_thread.start()
