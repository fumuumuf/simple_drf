Django いろいろお試し用プロジェクト

## 環境

Python 3.7 

### packages

[requirements.txt](apps/requirements.txt) を参照

## usage

### local

```shell
cd apps
pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

### use docker

```shell
docker-compose up
docker exec -it simple_drf bash 

# --- inner container ---

pip install -r requirements.txt
python manage.py runserver
```

#### use mysql

docker では mysql を使用できるようにしてる.

```shell
# --- inner container ---
cp sample.env .env

# cleanup mysql (初回のみ実行)
sh reset_mysql.sh 

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
