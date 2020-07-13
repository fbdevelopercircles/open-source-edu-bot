FROM python:3.7-alpine
LABEL MAINTAINER "Facebook Developers Circles" 

WORKDIR /app

COPY ./src .

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# CMD ["flask", "run"]