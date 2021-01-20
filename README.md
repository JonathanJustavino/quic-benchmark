# In this folder, we have a setup for a server-client pair, implemented in nodejs, which communicates either through a QUIC socket or a TCP socket with TLS

## Prerequisites

[dockerpy](https://docker-py.readthedocs.io/en/stable/):

```[bash]
pip3 install docker
```

[pythonping](https://pypi.org/project/pythonping/):

```[bash]
pip3 install pythonping
```

[pyshark](https://github.com/KimiNewt/pyshark): we recommend installing from repository

```[bash]
git clone https://github.com/KimiNewt/pyshark.git
cd pyshark/src
python setup.py install
```

[ttab](https://www.npmjs.com/package/ttab):

```[bash]
npm i ttab
```

## Run setup

### Run locally on machine

> Beware: Running the server and client locally only works if you have nodejs 15.6 in experimental mode already installed on your system

```[bash]
npm run tcp 
```

or

```[bash]
npm run quic
```

### Run in docker container

To run the setup in docker you do not have to have nodejs installed. instead the image, which is built from the [Dockerfile](Dockerfile) is pulled from [Dockerhub](https://hub.docker.com/r/ws2018sacc/experimentalnodejs).

```[bash]
sudo python3 run_server_client.py quic server
sudo python3 run_server_client.py quic client
```

or

```[bash]
sudo python3 run_server_client.py tcptls server
sudo python3 run_server_client.py tcptls client
```

> Beware: If you wish to build the image using the Dockerfile, take note, that it takes a very long time (up to 30 min), because nodejs has to be rebuilt in experimental mode

The script generates a json file with timestamps for every comparable event for tcp+tls and quic.

## Visualize Events: Plotting the result of the logfiles
The python script "visualize_events.py" in the folder visualize_events draws all given logfiles in the specified folder into one figure.
Currently, 4 logfiles are in the "measurements" folder, so it draws the timeline of these 4 logfiles into one figure.
