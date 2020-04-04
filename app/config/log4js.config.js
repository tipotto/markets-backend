const log4js = require("log4js");

let currentWorkingDirectory = process.cwd();
console.log("log4js.config.js: " + currentWorkingDirectory);

log4js.configure("./app/config/log4js.config.json");
const system = log4js.getLogger("system");
const http = log4js.getLogger("http");
const access = log4js.getLogger("access");

module.exports = {
  system,
  http,
  access
};
