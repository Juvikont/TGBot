Betonka1, [11.10.19 16:16]
FROM python:3-alpine

ENV BOT_ROOT=/opt/errbot

ADD requirements.txt $BOT_ROOT/requirements.txt

RUN apk add --no-cache libffi openssl git \
    && apk add --no-cache --virtual .build-deps \
           gcc \
           libc-dev \
           libffi-dev \
           openssl-dev \
    && pip install -r $BOT_ROOT/requirements.txt \
    && pip install slackclient python-telegram-bot \
    && apk del .build-deps

ADD . $BOT_ROOT

RUN addgroup -S errbot \
    && adduser -h $BOT_ROOT -G errbot -S errbot \
    && mkdir -p $BOT_ROOT/data $BOT_ROOT/plugins \
    && chown -R errbot:errbot $BOT_ROOT

USER errbot
WORKDIR /opt/errbot
CMD errbot


pyopenssl
markdown~=2.6.11,<3.0
git+https://github.com/errbotio/errbot@a0f35732484c8c0692e123c48653517cffa21a42
wolframalpha
github3.py~=1.0.0
IGitt==0.4.2.dev20181025081017
gitpython
ramlient