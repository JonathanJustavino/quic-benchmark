
const { createQuicSocket } = require('net');
const fs = require('fs');
const hexdump = require('hexdump-nodejs');

const key  = fs.readFileSync('certs/quic/server.key');
const cert = fs.readFileSync('certs/quic/server.crt');
const ca   = fs.readFileSync('certs/quic/server.csr');
const port = 1234;

var EventTimeStamps = {
  listening: '',
  session: '',
  keylog: '',
  secure: '',
  data: '',
  streamEnd: '',
  streamClose: '',
  socketClose: '',
}

var durations = {
  handshakeDurationInNs: '',
}

// Create the QUIC UDP IPv4 socket bound to local IP port 1234
const server_socket = createQuicSocket({ endpoint: { port } });

// Tell the socket to operate as a server_socket using the given
// key and certificate to secure new connections, using
// the fictional 'hello' application protocol.
server_socket.listen({ key, cert, alpn: 'hello' });

server_socket.on('listening', () => {
  EventTimeStamps.listening = new Date();
});
    
server_socket.on('session', (session) => {
  EventTimeStamps.session = new Date();
  
  session.on('keylog', (line) => {
    EventTimeStamps.keylog = new Date();
    console.log(hexdump(line));
  });

  session.on('secure', () => {
    EventTimeStamps.secure = new Date();
  });

  session.on('stream', (stream) => {
    stream.on('data', function(data) {
      EventTimeStamps.data = new Date();
      console.log('Received: %s [it is %d bytes long]',
      data.toString().replace(/(\n)/gm,""),
      data.length);
    });
    
    stream.on('end', () => {
      EventTimeStamps.streamEnd = new Date();
    });
    
    stream.on('close', () => {
      EventTimeStamps.streamClose = new Date();
      durations.handshakeDurationInNs = session.handshakeDuration.toString();
    });
  });
  
  session.on('close', () => {
    console.log("number of bytes received for the socket: " + server_socket.bytesReceived);
    console.log("number of bytes sent from the socket: " + server_socket.bytesSent);
    console.log("number of packets received for the socket: " + server_socket.packetsReceived);
    console.log("number of packets sent from the socket: " + server_socket.packetsSent);
    server_socket.close();
  });
});

server_socket.on('close', () => {
  EventTimeStamps.socketClose = new Date();
  const eventData = JSON.stringify(EventTimeStamps);
  const durationData = JSON.stringify(durations);
  const data = eventData + durationData
  fs.writeFile('./quic-benchmark-server.json', data, 'utf8', (err) => {
    if (err) {
      console.log(`Error writing file: ${err}`);
    } else {
      console.log(`File is written successfully!`);
    }
  });
});