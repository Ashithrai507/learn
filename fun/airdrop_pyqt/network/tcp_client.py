import socket

TCP_PORT = 6000


def send_message(ip, message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, TCP_PORT))
        sock.send(message.encode())
        sock.close()
    except Exception as e:
        print("Send failed:", e)
