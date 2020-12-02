FROM ubuntu:20.04

COPY quic-client.js quic-server.js tcp-tls-client.js tcp-tls-server.js ./
COPY certs/ certs/

RUN apt-get update && apt-get install -y \
    python3 \
    python3-distutils \
    g++ \
    make \
    git

RUN git clone https://github.com/nodejs/quic.git

RUN cd quic/ \
    && ./configure --experimental-quic \
    && make -j4 \
    && make install
