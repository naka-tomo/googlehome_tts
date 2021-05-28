from __future__ import print_function, unicode_literals
import pychromecast
from gtts import gTTS
import http.server
import socketserver
import threading
import time
from urllib.parse import urlparse, parse_qs, unquote

PORT = 8000
SERVER_IP = "192.168.0.103"
GOOGLE_HOME_IP = "192.168.0.50"

ghome = pychromecast.Chromecast( GOOGLE_HOME_IP  )
ghome.wait()
def say( text ):
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

def main():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), ServerHandler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

if __name__=="__main__":
    main()