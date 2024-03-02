#!/bin/bash

if [ ! -d ./chutti_env ]
then
  python3.12 -m venv chutti_env
fi

source ./chutti_env/bin/activate

python3 manage.py tailwind install
pip3 install -r requirements.txt
