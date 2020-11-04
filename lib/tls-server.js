"use strict";

var _http = _interopRequireDefault(require("http"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

var HOST = "127.0.0.1";
var PORT = 3000;

var server = _http["default"].createServer(function (req, res) {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World!\n');
});

server.listen(PORT, HOST, function () {
  console.log("Server running at http://${HOST}");
});