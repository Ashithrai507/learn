from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel,
    QVBoxLayout, QGridLayout, QFrame
)
from PyQt6.QtCore import Qt
from ui.chat_window import ChatWindow
from network.tcp_server import TCPServer

from network.discovery import DiscoveryThread
from models.device import Device


class DeviceTile(QFrame):
    def __init__(self, device, click_callback):
        super().__init__()
        self.device = device

        self.setFixedSize(140, 140)
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 14px;
            }
            QFrame:hover {
                background-color: #2a2a2a;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel("💻")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size: 36px;")

        label = QLabel(device.name)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: white;")

        layout.addWidget(icon)
        layout.addWidget(label)
        self.setLayout(layout)

        self.mousePressEvent = lambda e: click_callback(device)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyDrop")
        self.setMinimumSize(900, 600)
        self.setStyleSheet("background-color: #121212;")

        self.devices = {}

        central = QWidget()
        self.setCentralWidget(central)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        title = QLabel("PyDrop")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; color: white;")

        self.status = QLabel("Searching for nearby devices…")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet("color: #aaaaaa;")

        self.grid = QGridLayout()
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.main_layout.addWidget(title)
        self.main_layout.addWidget(self.status)
        self.main_layout.addLayout(self.grid)

        central.setLayout(self.main_layout)

        # Start discovery
        self.discovery = DiscoveryThread(username="Ashith")
        self.discovery.device_found.connect(self.add_device)
        self.discovery.start()
        # Start TCP server
        self.server = TCPServer()
        self.server.message_received.connect(self.receive_message)
        self.server.start()
        self.chat_windows = {}

    def add_device(self, info):
        device = Device(info["name"], ip, info["port"])
        tile = DeviceTile(device, self.open_chat)

        ip = info["ip"]

        if ip in self.devices:
            return

        print("Discovered device:", info)

        device = Device(info["name"], ip, info["port"])
        tile = DeviceTile(device.name)

        index = len(self.devices)
        row = index // 4
        col = index % 4

        self.grid.addWidget(tile, row, col)
        self.devices[ip] = tile

        self.status.setText("Nearby devices found")

    def open_chat(self, device):
        if device.ip not in self.chat_windows:
            chat = ChatWindow(device)
            self.chat_windows[device.ip] = chat
            chat.show()
        else:
            self.chat_windows[device.ip].show()


    def receive_message(self, ip, message):
        if ip in self.chat_windows:
            self.chat_windows[ip].receive(message)


    def closeEvent(self, event):
        self.discovery.stop()
        self.discovery.terminate()

        if hasattr(self, "server"):
            self.server.stop()
            self.server.terminate()

        event.accept()

