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

# Convert static asset files
python3 manage.py collectstatic --no-input

# Apply any outstanding database migrations
python3 manage.py migrate

# Add pre-commit hook
cat ./pre-commit.sh > ./.git/hooks/pre-commit
chmod +x ./.git/hooks/pre-commit
