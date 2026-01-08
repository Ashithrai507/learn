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
        self.setMinimumSize(450, 550)

        layout = QVBoxLayout()

        # Chat view
        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)
        self.chat_view.setStyleSheet("""
            QTextEdit {
                background-color: #121212;
                color: white;
                border: none;
                font-size: 15px;
            }
        """)

        # Input
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a message…")
        self.input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 15px;
            }
        """)
        self.input.returnPressed.connect(self.send)

        # Send button
        send_btn = QPushButton("Send")
        send_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 14px;
                background-color: #1e88e5;
                color: white;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
        """)
        send_btn.clicked.connect(self.send)

        layout.addWidget(self.chat_view)
        layout.addWidget(self.input)
        layout.addWidget(send_btn)
        self.setLayout(layout)

        # Load chat history
        self.load_history()

    # ---------- Load stored messages ----------
    def load_history(self):
        messages = self.db.load_messages(self.device.ip)
        for direction, msg in messages:
            self.add_bubble(msg, direction)

    # ---------- Message bubble ----------
    def add_bubble(self, message, direction):
        if direction == "sent":
            bubble = f"""
            <div style="text-align:right; margin:8px;">
                <div style="
                    display:inline-block;
                    background:#1e88e5;
                    color:white;
                    padding:10px 14px;
                    border-radius:14px;
                    max-width:70%;
                    font-size:15px;
                ">
                    {message}
                </div>
            </div>
            """
        else:
            bubble = f"""
            <div style="text-align:left; margin:8px;">
                <div style="
                    display:inline-block;
                    background:#2a2a2a;
                    color:white;
                    padding:10px 14px;
                    border-radius:14px;
                    max-width:70%;
                    font-size:15px;
                ">
                    {message}
                </div>
            </div>
            """

        self.chat_view.append(bubble)
        self.chat_view.verticalScrollBar().setValue(
            self.chat_view.verticalScrollBar().maximum()
        )

    # ---------- Send message ----------
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

    # ---------- Receive message ----------
    def receive(self, msg):
        self.db.save_message(self.device.ip, "received", msg)
        self.add_bubble(msg, "received")
