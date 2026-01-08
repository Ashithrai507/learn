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
        # Sender socket (broadcast only)
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Listener socket (receive only)
        listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("", DISCOVERY_PORT))
        listener.settimeout(1)

        payload = json.dumps({
            "name": self.username,
            "port": 6000,
            "os": platform.system()
        }).encode()

        while self.running:
            try:
                # Broadcast presence
                sender.sendto(payload, ("255.255.255.255", DISCOVERY_PORT))

                # Listen for others
                try:
                    data, addr = listener.recvfrom(1024)
                    info = json.loads(data.decode())

                    if info["name"] != self.username:
                        info["ip"] = addr[0]
                        self.device_found.emit(info)

                except socket.timeout:
                    pass

                time.sleep(BROADCAST_INTERVAL)

            except Exception as e:
                print("Discovery error:", e)

        sender.close()
        listener.close()

    def stop(self):
        self.running = False
