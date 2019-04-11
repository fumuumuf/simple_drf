#!/bin/bash

script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)

# create database
if [ `mysql -uroot -ppassword -h${DB_HOST} -e 'show databases' | grep ${DB_NAME}` ]; then
    mysql -uroot -ppassword -h${DB_HOST} -e "drop database ${DB_NAME};"
fi
mysql -uroot -ppassword -h${DB_HOST} -e "create database ${DB_NAME};"

python manage.py migrate
