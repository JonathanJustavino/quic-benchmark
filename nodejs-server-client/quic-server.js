
const { createQuicSocket } = require('net');
const fs = require('fs');

const key  = fs.readFileSync('certs/quic/server.key');
const cert = fs.readFileSync('certs/quic/server.crt');
const ca   = fs.readFileSync('certs/quic/server.csr');
const port = 1234;

// Create the QUIC UDP IPv4 socket bound to local IP port 1234
const server_socket = createQuicSocket({ endpoint: { port } });

// Tell the socket to operate as a server_socket using the given
// key and certificate to secure new connections, using
// the fictional 'hello' application protocol.
server_socket.listen({ key, cert, alpn: 'hello' });
    
server_socket.on('session', (session) => {
  console.log("a new QuicServerSession has been created");
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

server_socket.on('listening', () => {
  console.log("The QuicSocket has started listening for incoming QuicServerSessions");
  console.log(`listening on ${port}...`);
});

server_socket.on('busy', () => {
  if (server_socket.serverBusy)
    console.log('Server is busy');
  else
    console.log('Server is not busy');
});

server_socket.on('close', () => {
  console.log("QuicSocket has been destroyed and is no longer usable");
});

server_socket.on('endpointClose', () => {
  console.log("QuicEndpoint associated with the QuicSocket closes and has been destroyed");
});
  
server_socket.on('sessionError', (error, session) => {
  console.log("Error occurs processing an event related to a specific QuicSession instance");
  console.log('error:', error.message);
});

server_socket.on('ready', () => {
  console.log("QuicSocket has been bound to a local UDP port");
});

server_socket.on('error', () => {
  console.log("QuicSocket was destroyed with an error");
});