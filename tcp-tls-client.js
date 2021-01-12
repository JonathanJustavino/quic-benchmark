'use strict';

var tls = require('tls');
var fs = require('fs');
var net = require('net');

const PORT = 1337;
var HOST = "";

validateIP();

function validateIP() {
    if (process.argv.length < 3) {
        console.log("Too few arguments");
        process.exit();
    }

    var local = process.argv[2];
    var ip = process.argv[3];

    if(local == "true") {
        HOST = "localhost";
        return;
    }

    if (local == "false") {
        if (ip){
            HOST = ip;
        }
        else {
            HOST = '192.168.52.36';
        }
        return;
    }
    
    console.log("Wrong commandline argument");
    process.exit();
}

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

function validateIP() {
    if (process.argv.length < 3) {
        console.log("Too few arguments");
        process.exit();
    }

    var local = process.argv[2];

    if(local == "true") {
        HOST = "localhost";
        return;
    }

    if (local == "false") {
        HOST = '192.168.52.36';
        return;
    }
    
    console.log("Wrong commandline argument");
    process.exit();
}