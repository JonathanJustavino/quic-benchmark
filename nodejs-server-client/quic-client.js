const { createQuicSocket } = require('net');
const fs = require('fs');
const hexdump = require('hexdump-nodejs');

const key  = fs.readFileSync('certs/quic/server.key');
const cert = fs.readFileSync('certs/quic/server.crt');
const ca   = fs.readFileSync('certs/quic/server.csr');

const client_socket = createQuicSocket({
  client: {
    key,
    cert,
    ca,
    requestCert: true,
    alpn: 'hello'
  }
});

const client_session = client_socket.connect({
  address: '192.168.52.38',
  port: 1234,
});

client_session.on('secure', () => {
  const currentTime = new Date();
  console.log("\nTLS handshake has been completed");
  console.log(currentTime);
  
  const stream = client_session.openStream();
  stream.write("I am the client sending you a message..");
  
  stream.on('data', function(data) {
    const currentTime = new Date();
    console.log("\nReceived data through QuicStream");
    console.log(currentTime);
    console.log('\nReceived: %s [it is %d bytes long]',
    data.toString().replace(/(\n)/gm,""),
    data.length);
    console.log(stream.session)
  });

  stream.on('blocked', () => {
    const currentTime = new Date();
    console.log("\nthe QuicStream has been prevented from sending queued data for the QuicStream due to congestion control");
    console.log(currentTime);
  });

  stream.on('close', () => {
    const currentTime = new Date();
    console.log("\nQuicStream is completely closed and underlying resources have been freed");
    console.log(currentTime);
  });
});

client_session.on('stream', (stream) => {
  const currentTime = new Date();
  console.log("\na new QuicStream has been initiated by the connected peer");
  console.log(currentTime);
});

client_session.on('close', () => {
  const currentTime = new Date();
  console.log("\nQuicSession has been destroyed and is no longer usable");
  console.log(currentTime);
});

client_session.on('keylog', (line) => {
  const currentTime = new Date();
  console.log("\nkey material is generated or received by a QuicSession");
  console.log(hexdump(line));
  console.log(currentTime);
});

client_socket.on('session', (session) => {
  const currentTime = new Date();
  console.log("\na new QuicClientSession has been created");
  console.log(currentTime);
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