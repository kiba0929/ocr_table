## 動作環境
- Python 3.9
- Docker (docker-compose)
- GitHub Actions
  - unittest
  - flake8

## 開発環境
```
# 環境構築
$ docker-compose build
$ docker-compose up -d
$ docker-compose exec app pipenv install

# パッケージ追加
$ docker-compose exec app pipenv install パッケージ名

# スクリプト実行(pipenv shell環境へ)
$ docker-compose exec app bash
$ pipenv shell

# テスト
$ docker-compose exec app pipenv run python setup.py test
```

## ファイルの置き場所
```
#docxファイルの準備
data/data_docxに使いたいdocxファイルを1.docx-n.docxまで置いておく

# docxファイルの前処理
$ docker-compose exec app pipenv run python src/process.py
基本的にはdocxファイルを入れ替えた時に1回行う(それ以外では実行しない),txtのフォルダやファイルが作成される

data/data_txt/1/1.txtなどにtxtファイルが入っている

手動でtxtファイルを加工した場合には差し替えておく
```

## indexへの質問
```
# indexへの質問の実行
$ docker-compose exec app pipenv run python src/main.py
data/data_txtにフォルダが存在していれば実行可能

これを実行すると質問を入力する指示が出てくるのでその通りに行う

出力結果はlog/development.logに記載される
```