import datetime
import socket
import select


class EchoServer:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 1433
        self.server_addr = (self.host, self.port)

    def create_socket(self):
        """
        This funcion is for:1. Create socket.
                            2. Bind the socket to address.
                            3. Enable a server to accept connections.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.server_addr)
        self.server_socket.listen(2)

        return self.server_socket

    def create_connection(self, server_socket):
        conn, addr = server_socket.accept()
        print("Connection: ", addr, "---", datetime.datetime.now())
        conn.sendall(b"Please enter your nickname: ")
        conn_name = conn.recv(1024).decode()
        print(conn_name, " join the room.")
        socket_list.append(conn)
        guest_list[conn] = conn_name
        msg = "current members in chatroom are: " + \
            str(tuple(guest_list.values()))
        conn.sendall(msg.encode('utf-8'))


if __name__ == "__main__":
    socket_list = list()
    guest_list = dict()
    chat_room = EchoServer()
    server_socket = chat_room.create_socket()
    socket_list.append(server_socket)
    print('Server is running normally.')
    while True:
        rlist, wlist, elist = select.select(socket_list, [], [])
        if not rlist:
            print('TIMEOUT!')
            server_socket.shutdown()
            server_socket.close()
            break
        for socket_one in rlist:
            if socket_one is server_socket:
                chat_room.create_connection(server_socket)
            else:
                try:
                    print(guest_list[socket_one], " : ",
                          socket_one.recv(1024).decode())
                except Exception:
                    print(guest_list[socket_one], " leaved the room.")
                    socket_list.remove(socket_one)
                    del guest_list[socket_one]
