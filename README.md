# Komplexpraktikum quic-benchmark

A project comparing the performance of QUIC sockets with TCP sockets.

## Motivation

QUIC is a transport-layer protocol that was initially developed by Google and is currently developed and standardized by the IETF.
HTTP mapping with QUIC is called HTTP/3, the newest version of HTTP. Communication via QUIC is encrypted by default.  
The purpose of this project is performance measurement of the QUIC protocol and compare it with the transmission control protocol (TCP) in combination with the Transport Layer Security (TLS), because TCP does not communicate encrypted by default.

## Experiment setup

In the experiment, we implemented two different setups: Client-Server communication with QUIC and Client-Server communication with TCP+TLS.
We implemented both in rust and nodejs.
We decided to go with nodejs for the rest of the experiment, because it is possible to set up QUIC as a socket and also directly as HTTP/3.
Also the documentation in nodejs is more detailed.
Server and Client are currently running in a docker environment on one machine and communicate via localhost.

## Prerequisites

[dockerpy](https://docker-py.readthedocs.io/en/stable/):

```[bash]
pip3 install docker
```

[tshark](https://tshark.dev/setup/install/):

```[bash]
sudo apt-get install tshark
```

[pyshark](https://github.com/KimiNewt/pyshark):

```[bash]
pip3 install pyshark
```

[matplotlib](https://matplotlib.org/stable/index.html):

```[bash]
pip3 install matplotlib
```

[colored](https://gitlab.com/dslackw/colored):

```[bash]
pip3 install colored
```

## Run setup

Commands required to benchmark the sockets on your machine.

### Run locally on machine

> Beware: Running the server and client locally only works if you have nodejs 15.6 in experimental mode already installed on your system
> This is **not recommended**, use the docker setup instead.

```[bash]
npm run tcp 
```

or

```[bash]
npm run quic
```

### Run in docker container

To run the setup in docker you do not have to have nodejs installed. Instead the image, which is built from the [Dockerfile](Dockerfile) is pulled from [Dockerhub](https://hub.docker.com/r/ws2018sacc/experimentalnodejs).

#### Benchmark parameters

![setup parameters](./documentation/setup-parameters.png)

> Beware: If you wish to build the image using the Dockerfile, take note, that it takes a very long time (up to 30 min), because nodejs has to be rebuilt in experimental mode

The script generates a json file with timestamps for every comparable event for tcp+tls and quic.

## Visualize Events: Plotting the result of the logfiles

The python script "visualize_events.py" in the folder visualize_events draws all given logfiles in the specified folder into one figure.
Currently, 4 logfiles are in the "measurements" folder, so it draws the timeline of these 4 logfiles into one figure.
