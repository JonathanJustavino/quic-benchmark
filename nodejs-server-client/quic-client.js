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
  const currentTime = new Date();
  console.log("\na new QuicClientSession has been created");
  console.log(currentTime);
});

client.on('secure', () => {
  const currentTime = new Date();
  console.log("\nTLS handshake has been completed");
  console.log(currentTime);

  const stream = client.openStream();
  stream.write("I am the client sending you a message..");

  stream.on('data', function(data) {
    console.log('\nReceived: %s [it is %d bytes long]',
    data.toString().replace(/(\n)/gm,""),
    data.length);
    console.log(stream.session)
  });
  stream.on('error', (err) => console.error(err));
});

client_socket.on('close', () => {
  const currentTime = new Date();
  console.log("\nQuicSocket has been destroyed and is no longer usable");
  console.log(currentTime);
});

client_socket.on('endpointClose', () => {
  const currentTime = new Date();
  console.log("\nQuicEndpoint associated with the QuicSocket closes and has been destroyed");
  console.log(currentTime);
});
  
client_socket.on('sessionError', (error, session) => {
  const currentTime = new Date();
  console.log("\nError occurs processing an event related to a specific QuicSession instance");
  console.log('error:', error.message);
  console.log(currentTime);
});

client_socket.on('ready', () => {
  const currentTime = new Date();
  console.log("\nQuicSocket has been bound to a local UDP port");
  console.log(currentTime);
});

client_socket.on('error', () => {
  const currentTime = new Date();
  console.log("\nQuicSocket was destroyed with an error");
  console.log(currentTime);
});