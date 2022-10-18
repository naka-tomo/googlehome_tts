from __future__ import print_function, unicode_literals
import pychromecast
from pychromecast.socket_client import ConnectionStatusListener
from gtts import gTTS
import http.server
import socketserver
import threading
import time
from urllib.parse import urlparse, parse_qs, unquote

PORT = 8000
SERVER_IP = "192.168.0.155"


def connect_google_home():
    while 1:
        print("Try to connect Google Home. ")
        casts, browser = pychromecast.get_chromecasts()

        if len(casts)==0:
            print("Not found google home. Retry. ")
            time.sleep(1)
            continue

        ghome = casts[0]
        ghome.register_connection_listener(ConnectionWatcher())
        ghome.wait()
        browser.stop_discovery()
        return ghome


class ConnectionWatcher(ConnectionStatusListener):
    is_connected = False
    def new_connection_status(self, status):
        if status.status=="LOST":
            print("Lost connection. ")
            ConnectionWatcher.is_connected = False
        elif status.status=="CONNECTED":
            print("Connected. ")
            ConnectionWatcher.is_connected = True

def say( text ):
    if ghome is None:
        print("GoogleHome is not ready. ")
        return False

    if text.startswith("http"):
        # URLの場合はそのまま再生
        url = text
        print("play")
    else: 
        # 文字列の場合は音声ファイルに変換
        tts = gTTS(text=text, lang="ja")
        tts.save("tmp.mp3")

        url = "http://" + SERVER_IP + ":" + str(PORT) + "/tmp.mp3"
        print( url )

    ghome.media_controller.play_media( url, "audio/mp3")
    return True

class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_len  = int(self.headers.get("content-length"))
        req_body = self.rfile.read(content_len).decode("utf-8")
        req_body = unquote(req_body)

        print( "data", req_body )
        if req_body.startswith("text="):
            text = req_body[5:]
            print(text)
            say( text )

        body = "recieved"
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-length', len(body.encode()))
        self.end_headers()
        self.wfile.write(body.encode())

def server_thread():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), ServerHandler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

ghome = connect_google_home()
def main():
    global ghome

    th = threading.Thread( target=server_thread )
    th.daemon = True
    th.start()

    while 1:
        if ConnectionWatcher.is_connected==False:
            ghome.disconnect()
            ghome = None
            ghome = connect_google_home()

        time.sleep(0.1)

if __name__=="__main__":
    main()