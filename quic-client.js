const { createQuicSocket } = require('net');
const fs = require('fs');
const hexdump = require('hexdump-nodejs');

const key  = fs.readFileSync('certs/quic/server.key');
const cert = fs.readFileSync('certs/quic/server.crt');
const ca   = fs.readFileSync('certs/quic/server.csr');

var EventTimeStamps = {
  ready: '',
  writeToServer: '',
  error: '',
}

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

client_socket.on('ready', () => {
  EventTimeStamps.ready = new Date();
});

client_session.on('secure', () => {
  const stream = await client_session.openStream();

  EventTimeStamps.writeToServer = new Date();
  stream.write("I am the client sending you a message..");
  stream.end();
  client_socket.close();
  const data = JSON.stringify(EventTimeStamps);
  fs.writeFile('./quic-benchmark-client.json', data, 'utf8', (err) => {
    if (err) {
      console.log(`Error writing file: ${err}`);
    } else {
      console.log(`File is written successfully!`);
    }
  });
});

client_socket.on('error', () => {
  EventTimeStamps.error = new Date();
  console.log("\nQuicSocket was destroyed with an error");
});