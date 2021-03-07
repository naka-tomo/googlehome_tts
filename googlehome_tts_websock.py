# encoding: utf8
from __future__ import print_function, unicode_literals
from websocket_server import WebsocketServer
import pychromecast
from gtts import gTTS
import http.server
import socketserver
import threading
import time

"""
pip install websocket-server
pip install pychromecast
pip install gTTS
"""

ghome = None

def http_server_thread():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

def say(text):
    tts = gTTS(text=text, lang="ja")
    tts.save("tmp.mp3")

    ghome.media_controller.play_media("http://192.168.0.103:8000/tmp.mp3", "audio/mp3")

def message_received(client, server, message):
    # 日本語の文字コードがおかしいので修正
    message = bytes(message, "iso-8859-1").decode("utf8")
    print("recieved data:", message)
    if message.startswith("http"):
        ghome.media_controller.play_media(message, "audio/mp3")
    else:
        say(message)

def new_client(client, server):
    print("クライアント接続")

def client_left(client, server):
    print("クライアント切断")


def main():
    global ghome

    # httpサーバーを起動
    t = threading.Thread( target=http_server_thread )
    t.setDaemon(True)
    t.start()

    # googlehomeに接続
    ghome = pychromecast.Chromecast("192.168.0.50")
    ghome.wait()

    # webscoket serverを起動
    server = WebsocketServer(50000, host="192.168.0.103")
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received) 

    server.run_forever()

if __name__=="__main__":
    main()