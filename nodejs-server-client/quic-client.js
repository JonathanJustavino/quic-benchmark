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

client_socket.on('error', () => {
  const currentTime = new Date();
  console.log("\nQuicSocket was destroyed with an error");
  console.log(currentTime);
});

client_socket.on('close', () => {
  const currentTime = new Date();
  console.log("\nQuicSocket has been destroyed and is no longer usable");
  console.log(currentTime);
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
  console.log("\nsending message to server..");
  stream.write("I am the client sending you a message..");

  stream.on('blocked', () => {
    const currentTime = new Date();
    console.log("\nthe QuicStream has been prevented from sending queued data for the QuicStream due to congestion control");
    console.log(currentTime);
  });
});

client_session.on('close', () => {
  client_socket.close();
});