from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit,
    QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt

from network.tcp_client import SendMessageThread
from storage.chat_db import ChatDB


class ChatWindow(QWidget):
    def __init__(self, device):
        super().__init__()
        self.device = device

        self.db = ChatDB()
        self.send_threads = []

        self.setWindowTitle(f"Chat – {device.name}")
        self.setMinimumSize(420, 520)

        layout = QVBoxLayout()

        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)
        self.chat_view.setStyleSheet("background-color: #121212; color: white;")

        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a message…")
        self.input.returnPressed.connect(self.send)

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send)

        layout.addWidget(self.chat_view)
        layout.addWidget(self.input)
        layout.addWidget(send_btn)
        self.setLayout(layout)

        # Load chat history
        self.load_history()

    # ---------------- Load History ---------------- #
    def load_history(self):
        messages = self.db.load_messages(self.device.ip)
        for direction, msg in messages:
            self.add_bubble(msg, direction)

    # ---------------- Message Bubble ---------------- #
    def add_bubble(self, message, direction):
        if direction == "sent":
            bubble = f"""
            <div style="
                text-align: right;
                margin: 6px;
            ">
                <span style="
                    background:#1e88e5;
                    padding:8px;
                    border-radius:10px;
                    display:inline-block;
                    max-width:70%;
                ">
                    {message}
                </span>
            </div>
            """
        else:
            bubble = f"""
            <div style="
                text-align: left;
                margin: 6px;
            ">
                <span style="
                    background:#333333;
                    padding:8px;
                    border-radius:10px;
                    display:inline-block;
                    max-width:70%;
                ">
                    {message}
                </span>
            </div>
            """

        self.chat_view.append(bubble)

    # ---------------- Send ---------------- #
    def send(self):
        msg = self.input.text().strip()
        if not msg:
            return

        sender = SendMessageThread(self.device.ip, msg)
        self.send_threads.append(sender)
        sender.finished.connect(lambda: self.send_threads.remove(sender))
        sender.start()

        self.db.save_message(self.device.ip, "sent", msg)
        self.add_bubble(msg, "sent")
        self.input.clear()

    # ---------------- Receive ---------------- #
    def receive(self, msg):
        self.db.save_message(self.device.ip, "received", msg)
        self.add_bubble(msg, "received")
