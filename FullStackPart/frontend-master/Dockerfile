FROM ubuntu:16.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update && apt-get install -qqy \
    wget \
    bzip2 \
    libssl-dev \
    openssh-server \
    nodejs \
    npm \
    graphviz

RUN apt-get autoremove -y

# NodeJS
RUN npm install -g n
RUN n 9.11.1

RUN mkdir -p /frontend
RUN mkdir -p /app

RUN npm i
WORKDIR /app
COPY ./app/package.json /app/
RUN npm install
COPY ./app /app
RUN npm run build


WORKDIR /app

EXPOSE 8000
EXPOSE 22