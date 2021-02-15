'use strict';

var tls = require('tls');
var fs = require('fs');
var net = require('net');

const PORT = 1337;
var HOST = "";
const local_server = 'tcp-server';

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

function createClient(host, port, options) {
    return tls.connect(PORT, HOST, options, function() {});
}

function registerEventHandlers(client_socket) {
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

    client_socket.on('error', (error) => {
        EventTimeStamps.error = new Date();
        console.log("\nTLSSocket was destroyed with an error");
        console.log(error)
    });
}

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
        HOST = local_server;
        return;
    }
    
    console.log("Wrong commandline argument");
    process.exit();
}

validateIP();
var clientSocket = createClient(HOST, PORT, options);

console.log(`connecting to host: ${HOST}, port: ${PORT}`)

registerEventHandlers(clientSocket);
