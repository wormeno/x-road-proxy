FROM python:3.7
ENV PYTHONUNBUFFERED 1
WORKDIR    /opt/oracle
RUN        apt-get update && apt-get install -y libaio1 wget unzip \
            && ldconfig
WORKDIR /src
RUN mkdir /my_app_dir
WORKDIR /my_app_dir
COPY requirements.txt /my_app_dir/
RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt
COPY  . /my_app_dir/