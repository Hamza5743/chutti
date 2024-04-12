#!/bin/bash

source ./chutti_env/bin/activate

trap 'pkill -P $$' INT
LC_ALL="C" postgres -D /usr/local/var/postgresql@16 &> database.logs & python3 manage.py tailwind start > tailwind.logs & python3 manage.py runserver 0.0.0.0:10000
