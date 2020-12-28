const { createQuicSocket } = require('net');
const fs = require('fs');

const key  = fs.readFileSync('certs/quic/server.key');
const cert = fs.readFileSync('certs/quic/server.crt');
const ca   = fs.readFileSync('certs/quic/server.csr');

// Create a QuicSocket associated with localhost and port 2345
//const socket = createQuicSocket({ endpoint: { port: 2345 } });

const client_socket = createQuicSocket({
  client: {
    key,
    cert,
    ca,
    requestCert: true,
    alpn: 'hello'
  }
});

const client = client_socket.connect({
  address: '192.168.52.38',
  port: 1234,
});

client_socket.on('session', (session) => {
  console.log("a new QuicClientSession has been created");
  console.log(session.idleTimeout);
});

client.on('secure', () => {
  console.log("TLS handshake has been completed");
  const stream = client.openStream();

  stream.write("I am the client sending you a message..");
  stream.write("sending data..");

  stream.on('data', function(data) {
    console.log('Received: %s [it is %d bytes long]',
    data.toString().replace(/(\n)/gm,""),
    data.length);
    console.log(stream.session)
  });
  stream.on('error', (err) => console.error(err));
});

client_socket.on('close', () => {
  console.log("QuicSocket has been destroyed and is no longer usable");
});

client_socket.on('endpointClose', () => {
  console.log("QuicEndpoint associated with the QuicSocket closes and has been destroyed");
});
  
client_socket.on('sessionError', (error, session) => {
  console.log("Error occurs processing an event related to a specific QuicSession instance");
  console.log('error:', error.message);
});

client_socket.on('ready', () => {
  console.log("QuicSocket has been bound to a local UDP port");
});

client_socket.on('error', () => {
  console.log("QuicSocket was destroyed with an error");
});