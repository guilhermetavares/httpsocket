import socket
import base64
import re
import uuid
from urllib.parse import urlparse


class SocketHttp(object):
    
    def __init__(self, url, port=80):
        self.url = url
        self.port = 80
        self.url_parse = urlparse(url)
        self._connect()

    def assert_websocket(self):
        if self.url_parse.path == '/ws':
            return True

        if self.url_parse.scheme == 'ws':
            return True

        return False
    
    def send(self, data):
        data = str(data)
        return self.mysocket.send(bytes(data, 'utf-8'))
        
    def upgrade(self):
        KEY = base64.encodebytes(uuid.uuid4().bytes)
        data = bytes("\r\n".join([
            "GET {} HTTP/1.1".format(self.url_parse.path or '/'),
            "Upgrade: websocket",
            "Connection: Upgrade",
            "Host: {}".format(self.url_parse.netloc),
            "Origin: {}".format(self.url),
            "Sec-WebSocket-Key: {}".format(KEY.decode("utf-8")),
            "Sec-WebSocket-Version: 13",
            "",
            "",
        ]), 'utf-8')
        self._process(data)
    
    def http(self):
        data = bytes("\r\n".join([
            "GET {} HTTP/1.1".format(self.url_parse.path or '/'),
            "Host: {}".format(self.url_parse.netloc),
            "",
            "",
        ]), 'utf-8')
        self._process(data)
    
    def _process(self, data):
        self._sendall(data)
        response = self._response()
        self.response = response
        self.status_code = self._parse(response, 'HTTP/1.1 (.*?) ') or 0
        pieces = response.split('\r\n\r\n')
        headers = pieces[0]
        self.content = '\r\n\r\n'.join(pieces[1:])
        headers = headers.split('\r\n')
        self.headers = self._format_header(headers[1:])
    
    def _parse(self, data, key):
        try:
            return re.compile(key).findall(data)[0]
        except IndexError:
            return ''
        
    def _format_header(self, headers):
        data = dict()
        for item in headers:
            if item:
                key, value = re.split(": ", item)
                data[key] = value
        return data
        
    def _connect(self):
        info = socket.getaddrinfo(self.url_parse.netloc, 80, 0, 0, socket.SOL_TCP)[0]
        family, kind, address = info[0], info[1], info[4]
        mysocket = socket.socket(family, kind)
        # TODO: make setsockopt optionals
        mysocket.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        mysocket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 10)
        mysocket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 3)
        mysocket.connect(address)
        self.mysocket = mysocket
    
    def _close(self):
        self.mysocket.close()
        self.mysocket = None
    
    def _decode(self, value):
        try:
            return value.decode("utf-8")
        except UnicodeDecodeError:
            return None
    
    def _sendall(self, data):
        self.mysocket.sendall(data)
    
    def _response(self):
        response = ''
        while True:
            chunk = self.mysocket.recv(65536)
            print(chunk)
            if len(chunk) == 0:
                break
            else:
                decode_chunck = self._decode(chunk)
                if decode_chunck:
                    response += self._decode(chunk)
        return response