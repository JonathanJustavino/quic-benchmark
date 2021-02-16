FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-distutils \
    g++ \
    make \
    git \
    iputils-ping \
    sed \
    gawk \
    vim

RUN git clone https://github.com/nodejs/quic.git
RUN git clone https://github.com/richardimaoka/ping-to-json.git

RUN cd quic/ \
    && ./configure --experimental-quic \
    && make -j4 \
    && make install

RUN echo 'alias l="ls -alhS"' >> ~/.bashrc

RUN npm install hexdump-nodejs