FROM --platform=linux/amd64 gcr.io/oss-fuzz-base/base-builder-python:v1

RUN apt-get update -y && \
    apt-get install vim -y
