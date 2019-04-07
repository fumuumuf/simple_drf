Django いろいろお試し用プロジェクト

## 環境

Python 3.7 

### packages

[requirements.txt](/requirements.txt) を参照

## usage

```shell
pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

## 初期データ
テスト用データは, 各 app の `/fixutres/data.son` に配置する.

次のスクリプを実行することでロードされる.

```shell
python manage.py loaddata  ./*/fixtures/data.json
```

### ユーザーについて

初期データに以下のユーザーを用意している.

#### super user

ID: `admin`
PW: `hogehoge`

#### 一般

`admin` 以外のユーザー. PW はすべて `hogehoge`.
