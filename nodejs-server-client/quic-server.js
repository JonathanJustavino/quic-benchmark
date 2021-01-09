
const { createQuicSocket } = require('net');
const fs = require('fs');
const hexdump = require('hexdump-nodejs');

const key  = fs.readFileSync('certs/quic/server.key');
const cert = fs.readFileSync('certs/quic/server.crt');
const ca   = fs.readFileSync('certs/quic/server.csr');
const port = 1234;

var timeStamps = {
  handshakeDurationInNs: '',
}

// Create the QUIC UDP IPv4 socket bound to local IP port 1234
const server_socket = createQuicSocket({ endpoint: { port } });

// Tell the socket to operate as a server_socket using the given
// key and certificate to secure new connections, using
// the fictional 'hello' application protocol.
server_socket.listen({ key, cert, alpn: 'hello' });

server_socket.on('listening', () => {
  const currentTime = new Date();
  console.log("\nEvent 2: QuicSocket listening");
  console.log(currentTime);
});
    
server_socket.on('session', (session) => {
  const currentTime = new Date();
  console.log("\nEvent 3: QuicSession created");
  console.log(currentTime);
  
  session.on('keylog', (line) => {
    const currentTime = new Date();
    console.log("\nEvent 4: Key material generated or received");
    //console.log(hexdump(line));
    console.log(currentTime);
  });

  session.on('secure', () => {
    const currentTime = new Date();
    console.log("\nEvent 5: TLS handshake completed");
    console.log(currentTime);
  });

  session.on('stream', (stream) => {
    stream.on('data', function(data) {
      const currentTime = new Date();
      console.log("\nEvent 7: QuicStream received data");
      console.log(currentTime);
      console.log('Received: %s [it is %d bytes long]',
      data.toString().replace(/(\n)/gm,""),
      data.length);

    });
    
    stream.on('end', () => {
      const currentTime = new Date();
      console.log("\nEvent 8: End of QUICStream");
      console.log(currentTime);
    });
    
    stream.on('close', () => {
      const currentTime = new Date();
      console.log("\nEvent 9: QUICStream closed");
      console.log(currentTime);
      timeStamps.handshakeDurationInNs = session.handshakeDuration;
      console.log("handshake duration: " + timeStamps.handshakeDurationInNs);
    });
  });
  
  session.on('close', () => {
    const currentTime = new Date();
    console.log("\nEvent 10: QuicSession closed");
    console.log(currentTime);
    console.log("number of bytes received for the socket: " + server_socket.bytesReceived);
    console.log("number of bytes sent from the socket: " + server_socket.bytesSent);
    console.log("number of packets received for the socket: " + server_socket.packetsReceived);
    console.log("number of packets sent from the socket: " + server_socket.packetsSent);
    server_socket.close();
  });
});

server_socket.on('close', () => {
  const currentTime = new Date();
  console.log("\nEvent 11: QuicSocket closed");
  console.log(currentTime);
});