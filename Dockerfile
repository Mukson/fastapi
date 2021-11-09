# pull the official docker image
FROM python:3.8

# set work directory
WORKDIR /BostonGene_2_0

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .