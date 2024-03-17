#!/bin/bash

# Add Virtual Environment
if [ ! -d ./chutti_env ]
then
  python3.12 -m venv chutti_env
fi

source ./chutti_env/bin/activate

# Install dependencies
python3 manage.py tailwind install
pip3 install -r requirements.txt

# Add pre-commit hook
cat ./pre-commit.sh > ./.git/hooks/pre-commit
chmod +x ./.git/hooks/pre-commit
