FROM ubuntu:latest
MAINTAINER Yuri Kanapelka 'y.kanapelka@gmail.com'
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install python-telegram-bot
RUN pip install TelegramBotAPI
RUN pip install SQLAlchemy
COPY .. /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python crud.py

