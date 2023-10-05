FROM python:3.11-slim-buster as production

WORKDIR /app
ADD ./app/requirements.txt .

RUN apt-get update -y && \
    apt-get install git build-essential cmake pkg-config -y

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py", "/config/config.yaml" ]
