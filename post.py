# encoding: utf8

from __future__ import print_function, unicode_literals
import requests

url = "http://192.168.0.103:8000"
data = {"text":"こんにちは"}
req = requests.post(url, data=data)