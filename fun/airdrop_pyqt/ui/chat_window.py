from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit,
    QLineEdit, QPushButton, QLabel
)
from network.tcp_client import send_message


class ChatWindow(QWidget):
    def __init__(self, device):
        super().__init__()
        self.device = device

        self.setWindowTitle(f"Chat – {device.name}")
        self.setMinimumSize(400, 500)

        layout = QVBoxLayout()

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a message...")

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send)

        layout.addWidget(QLabel(device.name))
        layout.addWidget(self.chat_area)
        layout.addWidget(self.input)
        layout.addWidget(send_btn)

        self.setLayout(layout)

    def send(self):
        msg = self.input.text().strip()
        if not msg:
            return

        send_message(self.device.ip, msg)
        self.chat_area.append(f"You: {msg}")
        self.input.clear()

    def receive(self, msg):
        self.chat_area.append(f"{self.device.name}: {msg}")
