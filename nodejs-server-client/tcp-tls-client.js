'use strict';

var tls = require('tls');
var fs = require('fs');

const PORT = 1337;
const HOST = '192.168.52.36';

// Pass the certs to the server and let it know to process even unauthorized certs.
var options = {
    key: fs.readFileSync('certs/tcp-tls/private-key.pem'),
    cert: fs.readFileSync('certs/tcp-tls/public-cert.pem'),
    rejectUnauthorized: false
};
  
var client_socket = tls.connect(PORT, HOST, options, function() {
    // with tls.connect, the handshake is first completed before the socket can write to the server
    const currentTime = new Date();
    console.log("\nTLS handshake has been completed");
    console.log(currentTime);
    
    console.log("\nsending message to server..");
    client_socket.write("I am the client sending you a message..");
});

client_socket.on('end', () => {
    const currentTime = new Date();
    console.log('\nTLSSocket has been destroyed and is no longer usable');
    console.log(currentTime);
});

client_socket.on('error', () => {
    const currentTime = new Date();
    console.log("\nTLSSocket was destroyed with an error");
    console.log(currentTime);
  });
