'use strict';

var tls = require('tls');
var fs = require('fs');
var net = require('net');

const PORT = 1337;
const HOST = '192.168.52.36';

var options = {
    key: fs.readFileSync('certs/tcp-tls/private-key.pem'),
    cert: fs.readFileSync('certs/tcp-tls/public-cert.pem'),
    rejectUnauthorized: false,
};

var EventTimeStamps = {
    ready: '',
    writeToServer: '',
    error: '',
}

var client_socket = tls.connect(PORT, HOST, options, function() {});

client_socket.on('ready', () => {
    EventTimeStamps.ready = new Date();
});

client_socket.on('secureConnect', () => {
    EventTimeStamps.writeToServer = new Date();
    client_socket.write("I am the client sending you a message..");
    client_socket.end();

    const data = JSON.stringify(EventTimeStamps);
    fs.writeFile('./tcp-benchmark-client.json', data, 'utf8', (err) => {
        if (err) {
            console.log(`Error writing file: ${err}`);
        } else {
            console.log(`File is written successfully!`);
        }
    });
});

client_socket.on('error', () => {
    EventTimeStamps.error = new Date();
    console.log("\nTLSSocket was destroyed with an error");
});