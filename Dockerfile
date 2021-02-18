FROM ubuntu:20.04

COPY ./node/package.json package.json

RUN apt-get update && apt-get install -y \
    python3 \
    python3-distutils \
    g++ \
    make \
    git \
    iputils-ping \
    sed \
    gawk \
    vim \
    iproute2

RUN git clone https://github.com/nodejs/quic.git
RUN git clone https://github.com/richardimaoka/ping-to-json.git

RUN cd quic/ \
    && ./configure --experimental-quic \
    && make -j4 \
    && make install

RUN npm install