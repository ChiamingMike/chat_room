import socket
import select
import threading


class EchoClient:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 1433
        self.server_addr = (self.host, self.port)

    def connect_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(self.server_addr)
            print("Connected successfully.")

        except Exception:
            print("Failed to connect.")

    def listening(self):
        client_socket_list = [self.client_socket]
        while True:
            rlist, wlist, elist = select.select(client_socket_list, [], [])
            if self.client_socket in rlist:
                try:
                    msg = self.client_socket.recv(1024).decode()
                    print(msg)
                except Exception:
                    print("Failed to received message.")
                    exit()

    def speaking(self):
        while True:
            try:
                msg = input("text:")
                if msg == "exit":
                    print("You leaved the room.")
                    exit()
                self.client_socket.sendall(msg.encode("utf-8"))
            except Exception:
                print("Failed to type")
                exit()


if __name__ == "__main__":
    client = EchoClient()
    client.connect_socket()

    listen = threading.Thread(target=client.listening)
    listen.start()

    speak = threading.Thread(target=client.speaking)
    speak.start()
