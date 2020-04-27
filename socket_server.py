import socket
import threading
import logging

class SocketServer():
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 50007
        self.clients = []

    def socket_server_app(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(5)
        while True:
            try:
                conn, addr = sock.accept()
            except KeyboardInterrupt:
                break
            print("[接続]{}".format(addr))
            self.clients.append((conn, addr))
            thread = threading.Thread(target=self.handler, args=(conn, addr), daemon=True)
            thread.start()

    def close_connection(self, conn, addr):
        print('[切断]{}'.format(addr))
        conn.close()
        self.clients.remove((conn, addr))

    def handler(self, conn, addr):
        while True:
            try:
                data = conn.recv(1024)
            except ConnectionResetError:
                self.close_connection(conn, addr)
                break

            if not data:
                self.close_connection(conn, addr)
                break
            else:
                print('data : {}, addr&port: {}'.format(data, addr))
                for client in self.clients:
                    try:
                        client[0].sendto(data, client[1])
                        LOG_FILE = 'syslog.log'
                        logging.basicConfig(level=logging.INFO, format='%(data)s',
                                            datefmt='', filename=LOG_FILE, filemode='a')
                        logging.info(data)
                    except ConnectionResetError:
                        break

if __name__ == "__main__":
    ss = SocketServer()
    ss.socket_server_app()