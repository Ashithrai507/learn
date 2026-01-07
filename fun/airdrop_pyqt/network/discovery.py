import socket
import json
import time
import platform
from PyQt6.QtCore import QThread, pyqtSignal

DISCOVERY_PORT = 50000
BROADCAST_INTERVAL = 2


class DiscoveryThread(QThread):
    device_found = pyqtSignal(dict)

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.running = True

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("", DISCOVERY_PORT))
        sock.settimeout(1)

        payload = {
            "name": self.username,
            "port": 6000,
            "os": platform.system()
        }

        while self.running:
            try:
                # Broadcast presence
                sock.sendto(
                    json.dumps(payload).encode(),
                    ("<broadcast>", DISCOVERY_PORT)
                )

                # Listen for others
                data, addr = sock.recvfrom(1024)
                info = json.loads(data.decode())

                if info["name"] != self.username:
                    info["ip"] = addr[0]
                    self.device_found.emit(info)

            except socket.timeout:
                pass
            except Exception as e:
                print("Discovery error:", e)

            time.sleep(BROADCAST_INTERVAL)

        sock.close()

    def stop(self):
        self.running = False
