#!/bin/bash

source ./chutti_env/bin/activate

python3 manage.py makemigrations chutti
python3 manage.py migrate
