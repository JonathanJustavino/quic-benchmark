'use strict';

const tls = require('tls');
const fs = require('fs');
const hexdump = require('hexdump-nodejs');

const PORT = 1337;
var HOST = ""
const LOCALHOST = '0.0.0.0';

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
        HOST = LOCALHOST
        return;
    }
    
    console.log("Wrong commandline argument");
    process.exit();
}

var options = {
    key: fs.readFileSync('certs/tcp-tls/private-key.pem'),
    cert: fs.readFileSync('certs/tcp-tls/public-cert.pem')
};

const logFile = fs.createWriteStream('ssl-keys.log', { flags: 'a' });

var startHandshake
var endHandshake

function duration(startHandshake, endHandshake) {
    let first = (endHandshake[0] - startHandshake[0]) * 1000000000
    let second = (endHandshake[1] - startHandshake[1])
    return first + second
}

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

function createServer(host, port, options) {
    console.log(`Server running at: ${host}:${port}`)
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
    return server;
}

function registerEventHandler(server, keylogFlag) {
    server.on('connection', () => {
        startHandshake = process.hrtime();
        measurements.hrTimeStamps.beforeHandshake = startHandshake;
    });
    server.on('listening', function(error) { measurements.events.listening = new Date(); });
    
    server.on('newSession', (sessionID, sessionData, callback) => {
        measurements.events.session = new Date();
    });
    
    server.on('keylog', (line) => {
        measurements.events.keylog = new Date();
        if(keylogFlag) {
            console.log(hexdump(line));
        }
        logFile.write(line);
    });
    
    server.on('secureConnection', (socket) => {
        measurements.events.secure = new Date();
        endHandshake = process.hrtime();
        measurements.hrTimeStamps.afterHandshake = endHandshake;
        measurements.durations.handshakeDurationInNs = duration(startHandshake, endHandshake);
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
}

validateIP();
var server = createServer(HOST, PORT, options);
server.listen(PORT, HOST, function() {});
var keylogFlag = false;
registerEventHandler(server, keylogFlag);
