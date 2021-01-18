# Zu vergleichende Events

## QuicSocket

### QuicSocket - tls.Server

[x] 1. 'newSession'

### QuicSocket - tls.Socket

[x] 1. 'session'

### QuicSocket - Net.Server

[x] 1. 'listening'

### QuicSocket - Net.Socket

[x] 1. 'close'
[x] 2. 'ready'
   [ ] 1. Vergleich socket setup
[x] 3. 'error' - low priority
[ ] 4. bytesReceived() / bytesRead() (nicht vergleichbar, für quic ist es die socket und für tls der stream)
[ ] 5. bytesWritten() / bytesSend()

## QuicStream

### QuicStream - Duplex Stream (aber Vergleich auch TLS ebene)

[x] 1. 'close'
[x] 2. 'data'
[x] 3. 'end'
[ ] 4. 'readable' (calling readable stops data event from executing)

### QuicSession vs TLS?

[x] 1. 'secure'
[x] 2. 'keylog'
[x] 3. quicsession.handshakeDuration - Zeit messen keylog - secureConnection
[ ] 4. setzt session auf stream auf? oder anders rum? (close reihenfolge)

### QuicStream vs TLSStream

[x] 1. quicstream write - data
[ ] 2. tlsstream write ( secureConnect - data)
