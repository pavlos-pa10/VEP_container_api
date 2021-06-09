FROM ensemblorg/ensembl-vep

USER root
ENV PATH /usr/local/bin:$PATH

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3.8

    COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]