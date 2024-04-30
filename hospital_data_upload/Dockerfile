FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /code/requirements.txt
COPY ./src/ /app/

RUN pip install -r /code/requirements.txt

CMD ["sh", "entrypoint.sh"]

