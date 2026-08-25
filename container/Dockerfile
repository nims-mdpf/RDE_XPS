## Python Version:3.12
FROM python:3.12-slim-trixie


ARG PIP_TRUSTED_HOST

# Create app directory
WORKDIR /app

# Installation of wine
RUN dpkg --add-architecture i386 && apt update && apt install -y wine32
RUN apt-get update && apt-get -y install locales && localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG=ja_JP.UTF-8 LANGUAGE=ja_JP:ja LC_ALL=ja_JP.UTF-8 TZ=JST-9 TERM=xterm

# Installation of python's library
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy program or settings
COPY main.py /app
COPY modules/ /app/modules/
COPY modules_xps/ /app/modules_xps/
