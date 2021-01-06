FROM python:3-alpine 

MAINTAINER Chris Kreutzer <floyduww@gmail.com>

WORKDIR /meater

ADD meat_table.txt /meater
ADD meat_table_long.txt /meater
ADD meater_reader_buf.py /meater
ADD protobuf/meater_block.proto /meater/protobuf/
ADD protobuf/meater_block_pb2.py /meater/protobuf/


RUN apk add --update && \
    pip install paho.mqtt && \
    pip install requests && \
    pip install protobuf 

ENV HOME /meater
CMD ["python", "/meater/meater_reader_buf.py"]
