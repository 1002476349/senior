import socket
import threading
import os



class HttpWebServer(object):

    def __init__(self):
        server_socket = socket.socket()
        server_socket.bind(("", 9000))
        server_socket.listen(128)
        self.server_socket = server_socket


    def start(self):
        while True:
            new_client_socket, ip_port = self.server_socket.accept()
            sub_threading = threading.Thread(target=self.handle_socket, args=(new_client_socket, ip_port), daemon=True)
            sub_threading.start()

    @staticmethod
    def handle_socket(new_client_socket, ip_port):
        recv_data = new_client_socket.recv(4096)
        if len(recv_data) == 0:
            print("客户端下线了", ip_port)
            return
        recv_data = recv_data.decode("utf-8")
        path = recv_data.split(" ",2)[1]
        print(path)

        if path == "/":
            path = "/index.html"

        if os.path.exists("static" + path):

            with open("static" + path, "rb") as file:
                body = file.read()
            line = "HTTP/1.1 200 OK\r\n"
            head = "Server: HMS/1.0\r\n"
            blank = "\r\n"
            response_data = (line+head+blank).encode("utf-8") + body
            new_client_socket.send(response_data)
        else:
            with open("static/error.html", "rb") as file:
                body = file.read()
            line = "HTTP/1.1 404 Not Found OK\r\n"
            head = "Server: HMS/1.0\r\n"
            blank = "\r\n"
            response_data = (line+head+blank).encode("utf-8") + body
            new_client_socket.send(response_data)

        new_client_socket.close()

if __name__ == '__main__':
    server = HttpWebServer()
    server.start()
