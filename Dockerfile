FROM python:3.8
ENV PYTHONBUFFERED=1

RUN mkdir /hops
WORKDIR /hops
COPY requirements.txt /hops/
RUN pip install -r requirements.txt
COPY . /hops/