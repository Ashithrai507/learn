from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel,
    QVBoxLayout, QGridLayout, QFrame
)
from PyQt6.QtCore import Qt
from network.discovery import DiscoveryThread
from models.device import Device


class DeviceTile(QFrame):
    def __init__(self, name="Unknown Device"):
        super().__init__()
        self.setFixedSize(140, 140)
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 12px;
            }
            QFrame:hover {
                background-color: #2a2a2a;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        avatar = QLabel("💻")
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("font-size: 36px;")

        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("color: white;")

        layout.addWidget(avatar)
        layout.addWidget(name_label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyDrop")
        self.setMinimumSize(900, 600)

        self.devices = {}
        self.discovery = DiscoveryThread(username="Ashith")
        self.discovery.device_found.connect(self.add_device)
        self.discovery.start()


        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("PyDrop")
        title.setStyleSheet("font-size: 28px; color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Status
        self.status = QLabel("Searching for nearby devices…")
        self.status.setStyleSheet("color: #aaaaaa;")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Device grid
        self.grid = QGridLayout()
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)

        # TEMP: Dummy devices (for UI testing)
        for i in range(6):
            tile = DeviceTile(f"Device {i+1}")
            self.grid.addWidget(tile, i // 4, i % 4)

        main_layout.addWidget(title)
        main_layout.addWidget(self.status)
        main_layout.addLayout(self.grid)

        central.setLayout(main_layout)

        # Dark background
        self.setStyleSheet("background-color: #121212;")

    def add_device(self, info):
        ip = info["ip"]

        if ip in self.devices:
            return

        device = Device(info["name"], ip, info["port"])
        tile = DeviceTile(device.name)

        row = len(self.devices) // 4
        col = len(self.devices) % 4

        self.grid.addWidget(tile, row, col)
        self.devices[ip] = tile

        self.status.setText("Nearby devices found")

