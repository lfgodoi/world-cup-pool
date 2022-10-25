FROM python:3.9.9-slim

WORKDIR /app

COPY ./app /app

RUN apt update -y &&\
    apt upgrade -y &&\
    pip install --upgrade pip &&\
    pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["python", "main.py"]