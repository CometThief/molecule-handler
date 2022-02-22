# Dockerfile, Image, Container

FROM python:3.8-slim-buster

RUN mkdir -p /data/app

WORKDIR /data/app

RUN pip install requests numpy pandas tqdm scikit-learn tensorflow pymongo dnspython smilite pubchempy

#docker container run -it -v ${pwd}:/app test bash
