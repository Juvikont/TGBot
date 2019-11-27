FROM ubuntu:latest
MAINTAINER Yuri Kanapelka 'y.kanapelka@gmail.com'
RUN apt-get update
RUN apt-get install -y python3 python3-pip
COPY . /app
WORKDIR /app
RUN python3 -m pip install -r requirements.txt
CMD python3 main.py

