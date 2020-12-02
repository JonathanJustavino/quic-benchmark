
const { createQuicSocket } = require('net');
const fs = require('fs');

const key  = fs.readFileSync('../certs/quic/server.key');
const cert = fs.readFileSync('../certs/quic/server.crt');
const ca   = fs.readFileSync('../certs/quic/server.csr');
const port = 1234;

// Create the QUIC UDP IPv4 socket bound to local IP port 1234
const server = createQuicSocket({ endpoint: { port } });

// Tell the socket to operate as a server using the given
// key and certificate to secure new connections, using
// the fictional 'hello' application protocol.
server.listen({ key, cert, alpn: 'hello' });
    
server.on('session', (session) => {
  session.on('stream', (stream) => {
    stream.write("I am the server sending you a message.");

    stream.on('data', function(data) {
      console.log('Received: %s [it is %d bytes long]',
      data.toString().replace(/(\n)/gm,""),
      data.length);
      console.log(stream.session)
    });
  });
});

server.on('listening', () => {
  // The socket is listening for sessions!
  console.log(`listening on ${port}...`);
  console.log('input something!');
});