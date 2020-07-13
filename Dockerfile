FROM python:3.7-alpine
LABEL MAINTAINER "Facebook Developers Circles" 

RUN apk add --no-cache python3-dev libffi-dev gcc musl-dev make
RUN pip install gunicorn[gevent]

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /app
COPY ./src .

EXPOSE 5000

CMD gunicorn "fbosbot:create_app()" --worker-class gevent --workers 5 --bind 0.0.0.0:$PORT --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info
