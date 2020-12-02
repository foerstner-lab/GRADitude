FROM ubuntu:20.04
MAINTAINER Silvia Di Giorgio <digiorgio@zbmed.de>

RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get install -y build-essential gfortran libopenblas-dev liblapack-dev python3-matplotlib pkg-config libfreetype6 libfreetype6-dev libfreetype-dev cython3
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip3 install --upgrade setuptools
RUN pip3 install GRADitude==0.1.0

WORKDIR /root
