from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit,
    QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt

from network.tcp_client import SendMessageThread


class ChatWindow(QWidget):
    def __init__(self, device):
        super().__init__()
        self.device = device
        self.messages = []

        self.setWindowTitle(f"Chat – {device.name}")
        self.setMinimumSize(400, 500)

        layout = QVBoxLayout()

        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a message…")
        self.input.returnPressed.connect(self.send)

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send)

        layout.addWidget(self.chat_view)
        layout.addWidget(self.input)
        layout.addWidget(send_btn)

        self.setLayout(layout)

    def send(self):
        msg = self.input.text().strip()
        if not msg:
            return

        sender = SendMessageThread(self.device.ip, msg)
        sender.start()

        self.messages.append(("You", msg))
        self.chat_view.append(f"<b>You:</b> {msg}")
        self.input.clear()

    def receive(self, msg):
        self.messages.append((self.device.name, msg))
        self.chat_view.append(f"<b>{self.device.name}:</b> {msg}")
