#!/bin/bash

source ./chutti_env/bin/activate

python3 manage.py runserver & python3 manage.py tailwind start
