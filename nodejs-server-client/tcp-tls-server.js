'use strict';

var tls = require('tls');
var fs = require('fs');

const PORT = 1337;
const HOST = '127.0.0.1'

var options = {
    key: fs.readFileSync('certs/tcp-tls/private-key.pem'),
    cert: fs.readFileSync('certs/tcp-tls/public-cert.pem')
};

var server = tls.createServer(options, function(socket) {
    socket.write("I am the server sending you a message.");
    // Print the data that we received
    socket.on('data', function(data) {
        console.log('Received: %s [it is %d bytes long]',
            data.toString().replace(/(\n)/gm,""),
            data.length);
    });
});

// Start listening on a specific port and address
server.listen(PORT, HOST, function() {
    console.log("I'm listening at %s, on port %s", HOST, PORT);
});

server.on('error', function(error) {
    console.error(error);
    server.destroy();
});