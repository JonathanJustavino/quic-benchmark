# In this folder, we have a setup for a server-client pair, implemented in nodejs, which communicates either through a QUIC socket or a TCP socket with TLS

Prerequisites: [dockerpy](https://docker-py.readthedocs.io/en/stable/). It can be installed with:

```
pip3 install docker
```

To run he setup, execute the run_server_client.py file.
the setup file takes one parameter, that determines which kind of server-client-scenario is setup.

```
python3 run_server_client.py quic
python3 run_server_client.py tcptls
```

> Warning: building the image takes a very long time (up to 20 min), because nodejs has to be rebuild in experimental mode

The script generates a json file with timestamps for every comparable event for tcp+tls and quic.

## Visualize Events: Plotting the result of the logfiles
The python script "visualize_events.py" in the folder visualize_events draws all given logfiles in the specified folder into one figure.
Currently, 4 logfiles are in the "measurements" folder, so it draws the timeline of these 4 logfiles into one figure.
