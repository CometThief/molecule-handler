# Dockerfile, Image, Container

FROM python:3.8-slim-buster

RUN mkdir /app

WORKDIR /app

RUN pip install requests numpy pandas tqdm scikit-learn tensorflow

#docker container run -it -v ${pwd}:/app test bash
