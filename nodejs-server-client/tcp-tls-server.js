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

var measurements = {
    events: {
      listening: '',
      session: '',
      keylog: '',
      secure: '',
      data: '',
      streamEnd: '',
      streamClose: '',
      socketClose: '',
    },
    durations: {
      handshakeDurationInNs: '',
    },
    hrTimeStamps: {
        beforeHandshake: '',
        afterHandshake: '',
    },
}

var server = tls.createServer(options, function(socket) {
    socket.on('data', function(data) {
        measurements.events.data = new Date();
        console.log('Received: %s [it is %d bytes long]',
        data.toString().replace(/(\n)/gm,""),
        data.length);
    });

    socket.on('end', () => {
        measurements.events.streamEnd = new Date(); 
    });
    
    socket.on('close', () => {
        measurements.events.streamClose = new Date();
        server.close();
    });
});

server.on('connection', () => {
    measurements.hrTimeStamps.beforeHandshake = process.hrtime();
});

server.listen(PORT, HOST, function() {});

server.on('listening', function(error) {
    measurements.events.listening = new Date();
});

server.on('newSession', (sessionID, sessionData, callback) => {
    measurements.events.session = new Date();
});

server.on('keylog', (line) => {
    measurements.events.keylog = new Date();
    console.log(hexdump(line));
});

server.on('secureConnection', (socket) => {
    measurements.events.secure = new Date();
    measurements.hrTimeStamps.afterHandshake = process.hrtime();
    measurements.durations.handshakeDurationInNs = measurements.hrTimeStamps.afterHandshake[1] - measurements.hrTimeStamps.beforeHandshake[1];
});

server.on('close', () => {
    measurements.events.socketClose = new Date();
    const data = JSON.stringify(measurements);
    fs.writeFile('./tcp-benchmark-server.json', data, 'utf8', (err) => {
        if (err) {
            console.log(`Error writing file: ${err}`);
        } else {
            console.log(`File is written successfully!`);
        }
    });
});