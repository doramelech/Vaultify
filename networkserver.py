import socket
from datetime import datetime


class NetworkServer():
    __ip: str;
    __port: int;
    __server: socket.socket

    def __init__(self, ip="127.0.0.1", port=8000):
        self.__ip = ip
        self.__port = port

        self.__server = socket.socket()
        self.__server.bind((self.__ip, self.__port))
        self.__server.listen(1)
        print(f"server is up at {self.__ip}, {self.__port}")

    def start(self) -> None:
        try:
            client_socket, address = self.__server.accept()
            print(f"client connected, {address}")

            self.__handle_client(client_socket, address)
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.__server.close()
            print("Server says bye")

    def __handle_client(self, client_socket: socket.socket, address) -> None:
        try:
            while True:
                client_message = client_socket.recv(1024)

                if not client_message:
                    print(f"Client {address} disconnected.")
                    break

                decoded_msg = client_message.decode().strip()
                print(f"client says: {decoded_msg}")

                response_msg = self.__process(client_message)
                client_socket.send(response_msg.encode())

                if decoded_msg.upper() == "EXIT":
                    break

        except socket.error as e:
            print(f"Socket error with client {address}: {e}")
        finally:
            client_socket.close()

    def __process(self, msg: bytes) -> str:
        text = msg.decode().strip()
        parts = text.split(" ", 1)
        cmd = parts[0].upper()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "PING":
            return "PONG"
        elif cmd == "TIME":
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif cmd == "ECHO":
            return arg
        elif cmd == "EXIT":
            return "Goodbye!"
        else:
            return "ERROR"

if __name__ == "__main__":
    server = NetworkServer("127.0.0.1", 1729)
    server.start()