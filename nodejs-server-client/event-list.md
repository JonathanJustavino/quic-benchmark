# Zu vergleichende Events

## QuicSocket

### QuicSocket - tls.Server

1. 'newSession'

### QuicSocket - tls.Socket

1. 'session'

### QuicSocket - Net.Server

1. 'listening'

### QuicSocket - Net.Socket

1. 'close'
2. 'ready'
   1. Vergleich socket setup
3. 'error' - low priority
4. bytesReceived() / bytesRead()
5. bytesWritten() / bytesSend()

## QuicStream

### QuicStream - Duplex Stream (aber Vergleich auch TLS ebene)

1. 'close'
2. 'data'
3. 'end'
4. 'readable'

### QuicSession vs TLS?

1. 'secure'
2. 'keylog'
3. quicsession.handshakeDuration - Zeit messen keylog - secureConnection

### QuicStream vs TLSStream

1. quicstream write - data
2. tlsstream write ( secureConnect - data)
