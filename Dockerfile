#FROM python:3.7
FROM ubi8/s2i-base:rhel8.7
ENV PYTHONUNBUFFERED 1
WORKDIR    /app/
WORKDIR /src
RUN mkdir /my_app_dir
WORKDIR /my_app_dir
COPY requirements.txt /my_app_dir/
RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt
COPY  . /my_app_dir/