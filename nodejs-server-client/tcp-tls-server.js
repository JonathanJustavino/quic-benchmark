'use strict';

const tls = require('tls');
const fs = require('fs');
const hexdump = require('hexdump-nodejs');

const PORT = 1337;
// const HOST = '192.168.52.36';
const HOST = 'localhost';

var options = {
    key: fs.readFileSync('certs/tcp-tls/private-key.pem'),
    cert: fs.readFileSync('certs/tcp-tls/public-cert.pem')
};

var timeStamps = {
    beforeHandshake: '',
    afterHandshake: '',
    handshakeDurationInNs: '',
}

var server = tls.createServer(options, function(socket) {
    socket.on('data', function(data) {
        const currentTime = new Date();
        console.log("Event 7: TLSSocket received data");
        console.log(currentTime);
        console.log('Received: %s [it is %d bytes long]',
        data.toString().replace(/(\n)/gm,""),
        data.length);

    });

    socket.on('end', () => {
        const currentTime = new Date();
        console.log("\nEvent 8: End of TCPStream");
        console.log(timeStamps.afterHandshake);
        console.log(timeStamps.beforeHandshake);
        timeStamps.handshakeDuration = timeStamps.afterHandshake[1] - timeStamps.beforeHandshake[1];
        console.log(timeStamps);
    });
    
    socket.on('close', () => {
        const currentTime = new Date();
        console.log("\nEvent 9: TCPStream closed");
        console.log(currentTime);
        server.close();
    });
});

server.on('connection', () => {
    const timeBeforeHandshake = new Date();
    console.log("\nEvent connection: TCP Stream is established");
    timeStamps.beforeHandshake = process.hrtime();
    console.log(timeBeforeHandshake);
});

server.listen(PORT, HOST, function() {});

server.on('listening', function(error) {
    const currentTime = new Date();
    console.log("\nEvent 2: TLSServer listening");
    console.log(currentTime);
});

server.on('newSession', (sessionID, sessionData, callback) => {
    const currentTime = new Date();
    console.log("\nEvent 3: TLSSession created");
    console.log(currentTime);
});

server.on('keylog', (line) => {
    const currentTime = new Date();
    console.log("\nEvent 4: Key material generated or received");
    //console.log(hexdump(line));
    console.log(currentTime); 
});

server.on('secureConnection', (socket) => {
    const timeAfterHandshake = new Date();
    console.log("\nEvent 5: TLS handshake completed");
    timeStamps.afterHandshake = process.hrtime();
    console.log(timeAfterHandshake);
});

server.on('close', () => {
    const currentTime = new Date();
    console.log('\nEvent 11: TLSSocket closed');
    console.log(currentTime);
});