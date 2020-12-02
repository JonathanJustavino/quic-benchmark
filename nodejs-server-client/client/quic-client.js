const { createQuicSocket } = require('net');
const fs = require('fs');

const key  = fs.readFileSync('../certs/quic/server.key');
const cert = fs.readFileSync('../certs/quic/server.crt');
const ca   = fs.readFileSync('../certs/quic/server.csr');

// Create a QuicSocket associated with localhost and port 2345
//const socket = createQuicSocket({ endpoint: { port: 2345 } });

const socket = createQuicSocket({
  client: {
    key,
    cert,
    ca,
    requestCert: true,
    alpn: 'hello'
  }
});

const client = socket.connect({
  address: 'localhost',
  port: 1234,
});

client.on('session', (session) => {
  // The peer opened a new stream!
  console.log(session.idleTimeout);
});

client.on('secure', async () => {
  const stream = client.openStream();

  // to send user input to server
  //process.stdin.pipe(stream);
  
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
