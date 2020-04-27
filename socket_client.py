import socket
import threading
import socket_server
import random
import json

class SocketClient():
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 50007
        self.number = random.randint(0, 958)
        source = "item.json"
        json_open = open(source, 'r')
        item_list = json.load(json_open)
        data = item_list[self.number]["name"]
        self.label = data

    def socket_client_app(self):

        print('{}さん、こんにちは。'.format(self.label))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((self.host, self.port))
                thread = threading.Thread(target=self.handler, args=(sock,), daemon=True)
                thread.start()
                self.send_message(sock)
            except ConnectionRefusedError:
                print('ソケットサーバに接続を拒否されました。')
                print('ソケットサーバを立ち上げます。')
                print('Starting....')
                ss = socket_server.SocketServer()
                ss.socket_server_up()

    def send_message(self, sock):
        while True:
            try:
                msg = "[{}]".format(self.label) + input()
            except KeyboardInterrupt:
                msg = '{} さんが退出しました。Good Bye.'.format(self.label)
                sock.send(msg.encode('utf-8'))
                break
            if msg == '[{}]exit'.format(self.label):
                msg = '{} さんが退出しました。Good Bye.'.format(self.label)
                sock.send(msg.encode('utf-8'))
                break
            elif msg:
                try:
                    sock.send(msg.encode('utf-8'))
                except ConnectionRefusedError:
                    break
                except ConnectionResetError:
                    break

    def handler(self, sock):
        while True:
            try:
                data = sock.recv(1024)
                print("{}".format(data.decode("utf-8")))
            except ConnectionRefusedError:
                break
            except ConnectionResetError:
                break


if __name__ == "__main__":
    sc = SocketClient()
    sc.socket_client_app()