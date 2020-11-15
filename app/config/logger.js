var log4js = require('log4js');
// var logger = (exports = module.exports = {});

log4js.configure({
  appenders: {
    out: { type: 'stdout' },
  },
  categories: {
    default: { appenders: ['out'], level: 'debug' },
    errLog: { appenders: ['out'], level: 'error' },
  },
  //   appenders: [
  //     {
  //       type: "file",
  //       category: "request",
  //       filename: "request.log",
  //       pattern: "-yyyy-MM-dd"
  //     }
  //   ]
});

// logger.request = log4js.getLogger("request");
