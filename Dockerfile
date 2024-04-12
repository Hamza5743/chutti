FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN python3 manage.py collectstatic --no-input

CMD exec python3 manage.py runserver
