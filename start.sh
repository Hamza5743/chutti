#!/bin/bash

source ./chutti_env/bin/activate

trap 'pkill -P $$' INT
python3 manage.py runserver & python3 manage.py tailwind start
