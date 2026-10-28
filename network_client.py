import socket

class NetworkClient:
    def __init__(self,ip="127.0.0.1", port=8000):
        self.__sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((ip, port))

    def run(self) -> None:
        message = input("enter your message: (for exit enter EXIT)")

        while message.upper() != "EXIT":

            self.__sock.send(message.encode())

            print(f"Server says: {self.__sock.recv(1024).decode()}")

            message = input("enter your message: (for exit enter EXIT)")

        self.__sock.close()
