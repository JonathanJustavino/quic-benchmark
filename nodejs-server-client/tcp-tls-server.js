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

var hrTimeStamps = {
    beforeHandshake: '',
    afterHandshake: '',
}

var server = tls.createServer(options, function(socket) {
    socket.on('data', function(data) {
        EventTimeStamps.data = new Date();
        console.log('Received: %s [it is %d bytes long]',
        data.toString().replace(/(\n)/gm,""),
        data.length);
    });

    socket.on('end', () => {
        EventTimeStamps.streamEnd = new Date(); 
    });
    
    socket.on('close', () => {
        EventTimeStamps.streamClose = new Date();
        server.close();
    });
});

server.on('connection', () => {
    hrTimeStamps.beforeHandshake = process.hrtime();
});

server.listen(PORT, HOST, function() {});

server.on('listening', function(error) {
    EventTimeStamps.listening = new Date();
});

server.on('newSession', (sessionID, sessionData, callback) => {
    EventTimeStamps.session = new Date();
});

server.on('keylog', (line) => {
    EventTimeStamps.keylog = new Date();
    console.log(hexdump(line));
});

server.on('secureConnection', (socket) => {
    EventTimeStamps.secure = new Date();
    hrTimeStamps.afterHandshake = process.hrtime();
    durations.handshakeDurationInNs = hrTimeStamps.afterHandshake[1] - hrTimeStamps.beforeHandshake[1];
});

server.on('close', () => {
    EventTimeStamps.socketClose = new Date();
    const eventData = JSON.stringify(EventTimeStamps);
    const durationData = JSON.stringify(durations);
    const data = eventData + durationData
    fs.writeFile('./tcp-benchmark-server.json', data, 'utf8', (err) => {
        if (err) {
            console.log(`Error writing file: ${err}`);
        } else {
            console.log(`File is written successfully!`);
        }
    });
});