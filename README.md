# University project QUIC benchmarking

Comparing the performance of the QUIC protocol with a combination of the TCP+TLS protocols on the transport layer via sockets.

## Motivation

QUIC is a transport-layer protocol that was initially developed by Google and is currently developed and standardized by the [IETF](https://datatracker.ietf.org/wg/quic/about/).
HTTP mapping with QUIC is standardized in [HTTP/3](https://tools.ietf.org/html/draft-ietf-quic-http-32), the newest version of HTTP. Communication via QUIC is encrypted by default.  
The purpose of this project is the performance measurement of the QUIC protocol and compare it with the combination of the transmission control protocol (TCP) and the Transport Layer Security (TLS) protocol. The combination of TCP and TLS is necessary, as TCP does not use encryption by default.

## Experiment setup

The basis for our setup is the experimental [nodejs version 15.0.6](https://nodejs.org/download/release/v15.6.0/).
We decided to go with nodejs for this experiment because it is possible to set up QUIC as a socket and also directly as HTTP/3. Moreover, the documentation is really detailed.

In this experiment, we implemented two different Server-Client setups: One for communication via QUIC and the second for communication via TCP+TLS. Both implementations were installed into docker containers and uploaded to [dockerhub](https://hub.docker.com/r/ws2018sacc/experimentalnodejs). Using docker has several advantages:

* For reproducing the measurements, it is not necessary to download+compile nodejs in experimental mode.
* The experiment can be easily used on different operation systems
* Conducting the measurements is automated via docker-compose

A detailed depiction of the experiment is shown in [Topology](#topology)

The QUIC implementation of nodejs 15.0.6 is based on the QUIC IETF [draft-27](https://tools.ietf.org/html/draft-ietf-quic-transport-27).

The [draft-27](https://tools.ietf.org/html/draft-ietf-quic-transport-27) expired on 24 August 2020, the current deployable draft is [draft-32](https://tools.ietf.org/html/draft-ietf-quic-transport-32).
The differences between those two drafts are mainly restructuring of the text, more detailed explanation of some features and the style of figures is different.
Also the behaviour in some special cases has changed, i.e. "A server that chooses a zero-length connection ID MUST NOT provide a preferred address."
Because we always use the same connection setup in which these special cases do not occur, they are not relevant for our project.
In conclusion, the expired [draft-27](https://tools.ietf.org/html/draft-ietf-quic-transport-27) implementation of QUIC in nodejs is still sufficiently up to date to be used for our QUIC evaluation.

The QUIC documentation to our nodejs experimental version is available [here](https://nodejs.org/docs/v15.7.0/api/quic.html)

:red_circle: The experimental nodejs version we used is **no longer maintained**, as explained in this [commit](https://github.com/nodejs/node/pull/37067) in the official nodejs repository:
> The OpenSSL OMC has not yet committed to landing the updated QUIC APIs and has indicated that they will not even look at it until OpenSSL 3.1. With OpenSSL 3.0 > beta currently delayed with no clear idea of when it will actually land, the initial QUIC support landed in core has now just become a maintenance burden with
> no clear idea of when we'd ever be capable of delivering it. This PR, therefore, removes the QUIC support and reverts the patched in modifications to openssl. I > will be investigating a userland alternative that does not depend on the built-in openssl bindings.

This happened unfortunately after we were nearly finished with our project. Switching to another QUIC Server/Client architecture and do everything again would not have been possible on such a short notice.
As we built our own dockerimage with the nodejs version installed, it is still easily possible to run our project without having to get the now deprecated nodejs version from some archived nodejs repository.

## Topology

### Local Measurements

For the local measurements, we used a Thinkpad T480s with Ubuntu 20.04.2 LTS and ran the Client and Server on localhost. As described in [Experimental Setup](#experiment-setup), the client and server are running inside docker-containers.

*insert topology pic of local measurment*

### Remote Measurements

For the remote measurements, we used a MacBook11,3 with macOS 11.02.1 as Server and a Thinkpad T480s with Ubuntu 20.04.2 LTS as Client.  
Our Router only had the possibility to connect one LAN cable, because of this the Client had to be connected via WLAN. It is recommended to use LAN cable connections for both hosts if possible, because it reduces the network round trip time.

![topology](./documentation/topology.png)

## Prerequisites

[dockerpy](https://docker-py.readthedocs.io/en/stable/):

```[bash]
pip3 install docker
```

[tshark](https://tshark.dev/setup/install/):

```[bash]
sudo apt-get install tshark
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

### Run in docker container

To run the setup in docker you do not have to have nodejs installed. Instead the image, which is built from the [Dockerfile](Dockerfile) is pulled from [Dockerhub](https://hub.docker.com/r/ws2018sacc/experimentalnodejs).

#### Benchmark parameters

![setup parameters](./documentation/setup_parameters.png)

> Beware: If you wish to build the image using the Dockerfile, take note, that it takes a very long time (up to 30 min), because nodejs has to be rebuilt in experimental mode

The script generates a json file with timestamps for every comparable event for TCP+TLS and QUIC, as well as a packet capture via tshark and a json file documenting the ping output run simultaniously.

### Run locally on machine

> Beware: Running the server and client directly on your OS only works if you have nodejs 15.6 in experimental mode already installed on your system
> This is **not recommended**, use the docker setup instead.

```[bash]
npm run tcp
```

or

```[bash]
npm run quic
```

## Evaluation

The general structure of QUIC and TCP+TLS communication, based on network protocol layers:

![layers_comparison_QUIC_TCP](./documentation/layers_comparison_QUIC_TCP.png)

Both protocols work similar until they use TCP and UDP respectively in the transport layer.
Notably, the payload of the transport layer protocols is structured different: 
* **TCP+TLS**: The TLS layer is directly included in the TCP payload. Traffic control is managed by TCP.
* **QUIC:** The QUIC packet is included in the UDP payload. The encryption is also done via TLS, but the TLS CRYPTO frames are part of the QUIC payload. Traffic control is managed by QUIC. After exchanging encryption details via TLS, QUIC communication works with encrypted streams.


### Flowchart TCP+TLS

The communication between TCP+TLS Server and TCP+TLS Client is depicted in the following flowchart:

![tcp+tls_flowchart](./documentation/TCP_flowchart_to_pcap_2021-02-18_21_08_37.464861.png)

The TCP protocol contains following headerfields:
| Field Type | Size in Byte |
| --- | --- |
| Source Port | 2 |
| Destination Port | 2 |
| Sequence number | 4 |
| Acknowledgement number | 4 |
| Flags | 2 |
| Window size | 2 |
| TCP checksum | 2 |
| Urgent pointer | 2 |
| Options | 12 |
| |  Σ = 32 |

The overhead of the 

### Flowchart QUIC

The communication between QUIC Server and QUIC Client is depicted in the followin QUIC flowchart:

![quic_flowchart](./documentation/QUIC_flowchart_to_pcap_2021-02-18_19_57_03.396422.png)

QUIC frames are encapsulated in the payload of UDP packets.
The UDP protocol contains the following headerfields:
| Field Type | Size in Byte |
| Source port | 2 |
| Destination port | 2 |
| Length | 2 |
| Checksum | 2 |
| | Σ = 8 |

The QUIC protocol uses two types of headers: Long Header for the handshake and Short Header after the connection is established.
In the QUIC flowchart, each packet of the handshake (depicted with <span style="color:#9673A6">purple</span> arrows) has a QUIC long header, after the connection is established, each packet has a QUIC short header.

The Long Header contains the following headerfields:
| Field Type | Size in Byte |
| --- | --- |
| Header Form | 1 |
| Fixed Bit | 1 |
| Packet Type | 1 |
| Reserved Bits | 1 |
| Packet Nr. field length | 1 |
| Version | 4 |
| DCID length | 1 |
| DCIC | 20 |
| SCID length | 1 |
| SCID | 20 |
| Token length | 1 |
| Length of Packet Nr. + payload fields | 2 |
| Packet Nr. | 1 |
| | Σ = 55 |

The Short Header contains the following headerfields:
| Field Type | Size in Byte |
| --- | --- |
| Header Form | 1 |
| Fixed Bit | 1 |
| Spin Bit | 1 |
| Reserved Bit | 1 |
| Key Phase Bit | 1 |
| Packet Nr. length | 1 |
| DCID | 20 |
| Packet Nr. | 1 |
| | Σ = 27 |

There is an important difference with the usage of TLS between QUIC and TCP, as noted in [draft-ietf-QUIC-tls-27](https://tools.ietf.org/html/draft-ietf-QUIC-tls-27#section-4):

> One important difference between TLS records (used with TCP) and QUIC
> CRYPTO frames is that in QUIC multiple frames may appear in the same
> QUIC packet as long as they are associated with the same encryption
> level.  For instance, an implementation might bundle a Handshake
> message and an ACK for some Handshake data into the same packet.

This can be seen at the QUIC flowchart:
The second packet (20,103 ms) contains one QUIC frame including TLS Server Hello, and another QUIC frame including TLS encrypted extensions.
The fifth packet (92,746) contains one QUIC frame including TLS handshake finished, and another QUIC frame including a new connection ID.

### Event comparisons

![setup parameters](./documentation/events_comparison.png)
The events that occurred in the same sequence for QUIC and TCP, were picked to be compared by time difference.

### Time comparisons

For further comparison, we defined specific durations for the communication using the events mentioned before.

* **Handshake**: handshakeDuration
* **Time to first Byte**: secure -> data
* **Content Transfer**: data -> streamEnd
* **Close socket**: streamEnd -> socketClose

![socket_comparison](./documentation/socket_comparison.png)

If looking back at the package analysis, QUIC uses fewer packets for the TLS Handshake than TCP. What is noticeable in this graph, is that even though the number of transferred packets is fewer for QUIC, the total duration of the connection is actually longer compared to TCP.
We can think of two explanations for this result: 
Firstly, the different priorities when executing a network protocol in user-space and kernel-space. The QUIC protocol is implemented in user-space and the TCP protocol is implemented in kernel-space. User-space tasks have a lower priority in the execution sequence than kernel-space tasks. 
Secondly, the nodejs version 16.05 is an experimental build. The implementation for QUIC may not be 100% finished and we cannot be sure if this didn't affect our measurements.

Beside the **Handshake**, the remaining durations **Time to first Byte**, **Content Transfer** and  **Close socket** are lower with TCP/TLS than with QUIC. We also contribute this to the TCP kernel implementation.

#### Adding Delay

To see how the content transfer is affected by a slower connection, we added various network delays using [traffic control (TC)](https://linux.die.net/man/8/tc).

![delay_comparison](./documentation/delay_comparison.png)

With increased delay, we can see a linear increase for the duration of **Handshake**, **Time to first Byte** and **Content Transfer** for both TCP/TLS and QUIC.
QUIC has a steeper linear increase than TCP.
Most noticeable and surprising is the spike in the duration of **Close socket** for QUIC. We assume this is caused by the specific QUIC implementation in nodejs, as it is still in experimental state.

![delay_10](./documentation/delay_10.png)
![delay_20](./documentation/delay_20.png)
![delay_50](./documentation/delay_50.png)

## Future Work

Based on the results we obtained in our experiment and the features we managed to implement in the given time, we think it would be interesting to explore the following topics:

* **Simulation of packet loss with the [TC tool](https://linux.die.net/man/8/tc):** One of the main advantages of QUIC is the improved package loss handling. Therefore it is possible that increasing the packet loss during measurements leads to better results for QUIC.

* **Reusing the connection for sending more payload:** As the socket close event of the QUIC connection takes exceedingly more time than all other events, reusing the connection could benefit the QUIC performance.

* **Comparison of socket-based transport layer with HTTP/3 application layer:** It could be interesting to check the difference in performance when comparing socket layer implementation to application layer implementation.

* **Comparison of TCP+TLS and QUIC with QUIC executed in kernel-space:** We think that the biggest disadvantage of QUIC in comparison to TCP+TLS is its execution in the user-space, because of the lower priority. If both are compared while executed in kernel-space, QUIC might perform better.
