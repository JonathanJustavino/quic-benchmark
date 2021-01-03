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
    // Check if the authorization worked
    if (client_socket.authorized) {
        console.log("Connection authorized by a Certificate Authority.");
    } else {
        console.log("Connection not authorized: " + client_socket.authorizationError)
    }
    
    client_socket.write("I am the client sending you a message..");
    client_socket.write("sending data..");
    
    client_socket.end();
});

client_socket.on("data", function(data) {
    console.log('Received: %s [it is %d bytes long]',
        data.toString().replace(/(\n)/gm,""),
        data.length);
});

client_socket.on('close', function() {
    console.log("Connection closed");
});
