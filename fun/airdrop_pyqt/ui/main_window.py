import socket
import platform

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel,
    QVBoxLayout, QGridLayout, QFrame
)
from PyQt6.QtCore import Qt

from network.discovery import DiscoveryThread
from models.device import Device


class DeviceTile(QFrame):
    def __init__(self, device):
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyDrop")
        self.setMinimumSize(900, 600)
        self.setStyleSheet("background-color: #121212;")

        # UNIQUE device name (CRITICAL)
        self.device_name = f"{socket.gethostname()}-{platform.system()}"
        print("My device name:", self.device_name)

        self.devices = {}

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("PyDrop")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; color: white;")

        self.status = QLabel("Searching for nearby devices…")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet("color: #aaaaaa;")

        self.grid = QGridLayout()
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(title)
        layout.addWidget(self.status)
        layout.addLayout(self.grid)
        central.setLayout(layout)

        # Start discovery
        self.discovery = DiscoveryThread(self.device_name)
        self.discovery.device_found.connect(self.add_device)
        self.discovery.start()

    def add_device(self, info):
        ip = info["ip"]

        if ip in self.devices:
            return

        device = Device(info["name"], ip, info["port"])
        print("UI adding device:", device)

        tile = DeviceTile(device)
        index = len(self.devices)

        self.grid.addWidget(tile, index // 4, index % 4)
        self.devices[ip] = tile

        self.status.setText("Nearby devices found")

    def closeEvent(self, event):
        # HARD STOP – prevents freezing
        self.discovery.stop()
        self.discovery.terminate()
        event.accept()
