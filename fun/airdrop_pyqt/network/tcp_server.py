import socket
from PyQt6.QtCore import QThread, pyqtSignal

TCP_PORT = 6000


class TCPServer(QThread):
    message_received = pyqtSignal(str, str)  # sender_ip, message

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("", TCP_PORT))
        server.listen(5)

        while self.running:
            try:
                conn, addr = server.accept()
                data = conn.recv(1024).decode()
                if data:
                    self.message_received.emit(addr[0], data)
                conn.close()
            except:
                pass

        server.close()

    def stop(self):
        self.running = False
