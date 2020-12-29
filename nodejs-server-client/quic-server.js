
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
  const currentTime = new Date();
  console.log("\na new QuicServerSession has been created");
  console.log(currentTime);

  session.on('stream', (stream) => {
    stream.write("I am the server sending you a message.");

    stream.on('data', function(data) {
      console.log('\nReceived: %s [it is %d bytes long]',
      data.toString().replace(/(\n)/gm,""),
      data.length);
      console.log(stream.session)
    });
  });
});

server_socket.on('listening', () => {
  const currentTime = new Date();
  console.log("\nThe QuicSocket has started listening for incoming QuicServerSessions");
  console.log(`listening on ${port}...`);
  console.log(currentTime);
});

server_socket.on('busy', () => {
  const currentTime = new Date();
  if (server_socket.serverBusy)
    console.log('\nServer is busy');
  else
    console.log('\nServer is not busy');
  console.log(currentTime);
});

server_socket.on('close', () => {
  const currentTime = new Date();
  console.log("\nQuicSocket has been destroyed and is no longer usable");
  console.log(currentTime);
});

server_socket.on('endpointClose', () => {
  const currentTime = new Date();
  console.log("\nQuicEndpoint associated with the QuicSocket closes and has been destroyed");
  console.log(currentTime);
});
  
server_socket.on('sessionError', (error, session) => {
  const currentTime = new Date();
  console.log("\nError occurs processing an event related to a specific QuicSession instance");
  console.log('error:', error.message);
  console.log(currentTime);
});

server_socket.on('ready', () => {
  const currentTime = new Date();
  console.log("\nQuicSocket has been bound to a local UDP port");
  console.log(currentTime);
});

server_socket.on('error', () => {
  const currentTime = new Date();
  console.log("\nQuicSocket was destroyed with an error");
  console.log(currentTime);
});