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
