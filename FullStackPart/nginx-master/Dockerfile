FROM nginx:1.11.9

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update && apt-get install -y wget bzip2

RUN echo 'export PATH=/opt/miniconda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/miniconda && \
    rm ~/miniconda.sh

ENV PATH /opt/miniconda/bin:$PATH
RUN pip install jinja2==2.9.4

COPY ./htpasswd /
COPY config/default.conf /templates/
COPY ./render_template.py /templates/
COPY ./start.sh /
RUN chmod +x start.sh
