const accessLogger = require("../config/log4js.config.js").access;

module.exports = (req, res, next) => {
  if (!req || !req.method || !req.headers) {
    // next();
    // accessLogger.error("The request doesn't have necessary parameters.");
    return;
  }

  if (req.method === "GET" || req.method === "DELETE") {
    accessLogger.info(req.query);
  } else {
    accessLogger.info(req.body);
  }
  next();
};
