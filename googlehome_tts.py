from __future__ import print_function, unicode_literals
import pychromecast
from gtts import gTTS
import http.server
import socketserver
import threading
import time

"""
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

    ghome.media_controller.play_media("http://192.168.0.9:8000/tmp.mp3", "audio/mp3")


def main():
    global ghome

    # httpサーバーを起動
    t = threading.Thread( target=http_server_thread )
    t.setDaemon(True)
    t.start()

    # googlehomeに接続
    ghome = pychromecast.Chromecast("192.168.0.50")
    ghome.wait()

    say("テスト")

    time.sleep(5)
    print("終了")


if __name__=="__main__":
    main()