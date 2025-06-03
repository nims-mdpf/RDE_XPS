# Python Version: 3.11
# python:3.11-slim-bookworm for linux/amd64
FROM python@sha256:fc39d2e68b554c3f0a5cb8a776280c0b3d73b4c04b83dbade835e2a171ca27ef

# Create app directory
WORKDIR /app

# Installation of wine
RUN dpkg --add-architecture i386 && apt update && apt install -y wine32
RUN apt-get update && apt-get -y install locales && localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG=ja_JP.UTF-8 LANGUAGE=ja_JP:ja LC_ALL=ja_JP.UTF-8 TZ=JST-9 TERM=xterm

# Installation of python's library
COPY requirements.txt /app
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --upgrade pip
RUN pip install -r requirements.txt

# Copy program or settings
COPY main.py /app
COPY modules/ /app/modules/
COPY modules_xps/ /app/modules_xps/
