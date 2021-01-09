'use strict';

var tls = require('tls');
var fs = require('fs');
var net = require('net');

const PORT = 1337;
// const HOST = '192.168.52.36';
const HOST = 'localhost';

var options = {
    key: fs.readFileSync('certs/tcp-tls/private-key.pem'),
    cert: fs.readFileSync('certs/tcp-tls/public-cert.pem'),
    rejectUnauthorized: false,
};

var client_socket = tls.connect(PORT, HOST, options, function() {});

client_socket.on('ready', () => {
    const currentTime = new Date();
    console.log("\nEvent 1: TLSSocket ready");
    console.log(currentTime);
});

client_socket.on('secureConnect', () => {
    const currentTime = new Date();
    client_socket.write("I am the client sending you a message..");
    console.log("\nEvent 6: TLSClient writes to TLSServer");
    console.log(currentTime);
    client_socket.end();
});

client_socket.on('error', () => {
    const currentTime = new Date();
    console.log("\nEvent x: TLSSocket was destroyed with an error");
    console.log(currentTime);
});