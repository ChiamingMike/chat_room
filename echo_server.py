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
        This funcion is for:1. Creating socket.
                            2. Binding the socket to address.
                            3. Enabling a server to accept connections.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.server_addr)
        self.server_socket.listen(2)

        return self.server_socket

    def create_connection(self, server_socket):
        """
        This function is for:4. Acceptinig a connection.
                             5. Sending data to the socket.
                             6. Receiving data from the socket.
        """
        conn, addr = server_socket.accept()
        print("New connection: ", addr, "at",
              datetime.datetime.now().strftime("%H:%M:%S"))
        conn.sendall(b"Please enter your nickname: ")
        conn_name = conn.recv(1024).decode()
        print(conn_name, " joined the room.")
        socket_list.append(conn)
        user_list[conn] = conn_name
        msg = "Current members in chatroom are: " + \
            str(tuple(user_list.values()))
        conn.sendall(msg.encode('utf-8'))
        conn.sendall(b"Hint: Typing 'exit' can leave the room.")


if __name__ == "__main__":
    socket_list = list()
    user_list = dict()
    chat_room = EchoServer()
    server_socket = chat_room.create_socket()
    socket_list.append(server_socket)
    print('Server is running normally.')
    while True:
        rlist, wlist, elist = select.select(socket_list, [], [], 60)
        if not rlist:
            # Automatically closing a socket file descriptor
            # when no one is using chat room.
            print('Timeout!')
            server_socket.close()
            break
        for socket_one in rlist:
            if socket_one is server_socket:
                chat_room.create_connection(server_socket)
            else:
                try:
                    print(user_list[socket_one], " : ",
                          socket_one.recv(1024).decode())
                except Exception:
                    # Notifying people that someone close the chat window.
                    # Also remove user from the user_list.
                    print(user_list[socket_one], " leaved the room.")
                    socket_list.remove(socket_one)
                    del user_list[socket_one]
