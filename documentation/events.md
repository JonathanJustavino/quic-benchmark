# Node.js events

This file provides the explanation for the events we timestamped and are using in our "visualize-events/graphs".

## ready

Quic Socket des Clients wurde an einen UDP Port gebunden

## session

Quic Server Session has been created

## secure

Quic Session declares TLS Handshake has been completed

## data

Quic Stream receives data

## streamEnd

Quic Stream has ended, all data received

## streamClose

QuicStream has is completely closed and the underlying resources have been freed

## socketClose

QuicSocket has been destroyed and is no longer usable
