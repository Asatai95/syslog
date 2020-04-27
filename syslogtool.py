from datetime import datetime, timezone, timedelta
import argparse
import logging
import socketserver
import pysyslogclient

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-mode", "--mode", default="CLI", help="action mode:CLI(default) or SERVER")
PARSER.add_argument("-i", "--ip", default="127.0.0.1", help="IP or hostname(default localhost)")
PARSER.add_argument("-p", "--port", default="12345", help="port number(default 514)")
PARSER.add_argument("-pr", "--protocol", default="UDP", help="TCP or UDP(default)")
PARSER.add_argument("-c", "--count", default="1", help="send count(default 1)")
PARSER.add_argument("-m", "--message", default="syslog message!!", help="syslog message")

class SyslogUDPHandler(socketserver.BaseRequestHandler):
    LOG_FILE = 'syslog.log'
    logging.basicConfig(level=logging.INFO, format='%(message)s',
                        datefmt='', filename=LOG_FILE, filemode='a')

    def handle(self):
        data = bytes.decode(self.request[0].strip())
        datalist = str(data).split(" ")
        datalist[1] = applytimezonejst(datalist[1])
        message = " ".join(datalist)

        socket = self.request[1]
        print(f"{self.client_address[0]}: {message}")
        logging.info(message)

def applytimezonejst(utcdate):
    _dt = datetime.strptime(utcdate, "%Y-%m-%dT%H:%M:%S.%fZ")
    _dt2 = _dt.replace(tzinfo=timezone.utc)\
            .astimezone(timezone(timedelta(hours=9)))\
            .strftime("%Y/%m/%d %H:%M:%S %Z %z")
    return _dt2

def syslogserver(host, port):
    try:
        server = socketserver.UDPServer((host, int(port)), SyslogUDPHandler)
        print(f"start syslog server ({host}:{port})")
        server.serve_forever(poll_interval=0.5)

    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down.")

def syslogclient(host, port, prot, count, message):
    client = pysyslogclient.SyslogClientRFC5424(host, port, proto=prot)

    for i in range(int(count)):
        client.log(message)
        print(f"sendcount:{str(i+1)}")

def main():
    optargs = PARSER.parse_args()
    mode = optargs.mode
    host = optargs.ip
    port = optargs.port
    prot = optargs.protocol
    count = optargs.count
    message = optargs.message

    if mode == "CLI":
        syslogclient(host, port, prot, count, message)
    else:
        syslogserver(host, port)

if __name__ == '__main__':
    main()
