const { createQuicSocket } = require('net');
const fs = require('fs');
const hexdump = require('hexdump-nodejs');

const key  = fs.readFileSync('certs/quic/server.key');
const cert = fs.readFileSync('certs/quic/server.crt');
const ca   = fs.readFileSync('certs/quic/server.csr');
const local_server = 'quic-server';
const PORT = 1234;
var HOST;

var EventTimeStamps = {
  ready: '',
  writeToServer: '',
  error: '',
}

function validateIP() {
  if (process.argv.length < 2) {
      console.log("Too few arguments");
      process.exit();
  }

  var ip = process.argv[2];
  var ipRegex = /\d{2,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/;
  var localIpRegex = /local/;

  if (ipRegex.test(ip)) {
      HOST = ip;
      return;
  }

  if (ip == null) {
      HOST = local_server;
      return;
  }
  
  console.log("Wrong commandline argument");
  process.exit();
}

function createClient() {
  return createQuicSocket({
    client: {
      key,
      cert,
      ca,
      requestCert: true,
      alpn: 'hello'
    }
  });
}

function createClientSession(client_socket, host) {
  return client_socket.connect({
    address: host,
    port: 1234,
  });
}

function registerSocketEventHandler(client_socket) {
  client_socket.on('ready', () => {
    EventTimeStamps.ready = new Date();
  });

  client_socket.on('error', () => {
    EventTimeStamps.error = new Date();
    console.log("\nQuicSocket was destroyed with an error");
  });
}

function registerSessionEventHandler(client_socket, client_session){
  client_session.on('secure', async () => {
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
}

validateIP();
var client = createClient();
registerSocketEventHandler(client);
var client_session = createClientSession(client, HOST);

console.log(`connecting to host: ${HOST}, port: ${PORT}`)

registerSessionEventHandler(client, client_session);