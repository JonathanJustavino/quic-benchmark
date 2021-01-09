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
  // address: '192.168.52.38',
  address: 'localhost',
  port: 1234,
});

client_socket.on('ready', () => {
  const currentTime = new Date();
  console.log("\nEvent 1: QuicSocket ready");
  console.log(currentTime);
});

client_session.on('secure', () => {
  const stream = client_session.openStream();

  const currentTime = new Date();
  stream.write("I am the client sending you a message..");
  console.log("\nEvent 6: QuicClient writes to QuicServer");
  console.log(currentTime);
  stream.end();
  client_socket.close();
});

client_socket.on('error', () => {
  const currentTime = new Date();
  console.log("\nEvent x: QuicSocket was destroyed with an error");
  console.log(currentTime);
});