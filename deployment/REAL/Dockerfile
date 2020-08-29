FROM continuumio/miniconda:latest
#FROM python:3

EXPOSE 5000

RUN mkdir /app
WORKDIR /app

COPY requirements.yml /app/requirements.yml
#RUN pip install -r requirements.yml
RUN conda env create -f /app/requirements.yml

ENV PATH /opt/conda/envs/revealapp/bin:$PATH

ENV PYTHONDONTWRITEBYTECODE 1

RUN echo "export PATH=$PATH" >> ~/.bashrc

RUN echo "source activate $(head -1 /app/requirements.yml | cut -d' ' -f2)" >> ~/.bashrc

COPY . /app

CMD python app.py