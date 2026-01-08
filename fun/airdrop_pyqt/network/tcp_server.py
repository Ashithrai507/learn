import socket
from PyQt6.QtCore import QThread, pyqtSignal

TCP_PORT = 6000


class TCPServer(QThread):
    message_received = pyqtSignal(str, str)  # ip, message

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", TCP_PORT))
        server.listen(5)
        server.settimeout(1)

        while self.running:
            try:
                conn, addr = server.accept()
                data = conn.recv(4096).decode()
                if data:
                    self.message_received.emit(addr[0], data)
                conn.close()
            except socket.timeout:
                pass
            except Exception as e:
                print("TCP server error:", e)

        server.close()

    def stop(self):
        self.running = False
