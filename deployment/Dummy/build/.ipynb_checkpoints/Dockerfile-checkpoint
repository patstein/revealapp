FROM continuumio/miniconda:latest

RUN apt-get update

ADD ./build/requirements.yml /tmp/requirements.yml

RUN conda env create -f /tmp/requirements.yml

ENV PATH /opt/conda/envs/syntheticus/bin:$PATH

ENV PYTHONDONTWRITEBYTECODE 1

RUN echo "export PATH=$PATH" >> ~/.bashrc

# Pull the environment name out of the requirements.yml
RUN echo "source activate $(head -1 /tmp/requirements.yml | cut -d' ' -f2)" >> ~/.bashrc

RUN mkdir -p /app && mkdir /app/logs && mkdir /app/data

COPY ./src /app/src

WORKDIR /app/src

