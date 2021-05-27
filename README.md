# GoogleHome TTS

Python実装の[Google Home Notifier](https://github.com/noelportugal/google-home-notifier)的なもの．GoogleHomeをしゃべらせたり，GoogleHomeで音楽を再生できます．

## インストール

```
pip3 install pychromecast
pip3 install gTTS
git clone https://github.com/naka-tomo/googlehome_tts.git
```

googlehome_tts.pyの上部のIPの設定を自身の環境に合わせて変更．

```
PORT = 8000  # このPythonスクリプトが利用するポート番号
SERVER_IP = "192.168.0.103" # サーバー（このPythonスクリプトが実行されるPC）のIP
GOOGLE_HOME_IP = "192.168.0.50"  # GoogleHomeのIPアドレス
```


## 実行

- サーバーを起動：
  ```
  cd googlehome_tts
  python googlehome_tts.py
  ```

- GoogleHomeをしゃべらせる場合：
  ```
  curl -X POST -d "text=hello" http://（サーバーのIP）:（ポート）
  ```

- GoogleHomeでWeb上のMP3(http://****/hoge.mp3)を再生する場合：
  ```
  curl -X POST -d "text=http://****/hoge.mp3" http://（サーバーのIP）:（ポート）
  ```

- GoogleHomeでローカルなMP3を再生する場合：  
  MP3ファイル（hoge.mp3）をgooglehome_tts.pyと同じディレクトリにコピー
  ```
  curl -X POST -d "text=http://（サーバーのIP）:（ポート）/hoge.mp3" http://（サーバーのIP）:（ポート）
  ```

- その他の送信方法  
　　- [pythonスクリプトから送信](post.py)  
　　- [htmlから送信](post.html)
