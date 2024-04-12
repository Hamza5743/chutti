#!/bin/bash

source ./chutti_env/bin/activate

trap 'pkill -P $$' INT
python3 manage.py runserver 0.0.0.0:10000 & python3 manage.py tailwind start
