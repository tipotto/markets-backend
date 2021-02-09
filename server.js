const cluster = require('cluster');
const express = require('express');
const cors = require('cors');
const logger = require('./app/config/log4js.config.js');
const SearchController = require('./app/controllers/search.controller.js');
const numCPUs = require('os').cpus().length;

console.log('numCPUs >>>', numCPUs);

if (cluster.isMaster) {
  console.log('Master');

  for (var i = 0; i < numCPUs; i++) {
    console.log(`Master : Cluster Fork ${i}`);
    // Create a worker
    cluster.fork();
  }

  cluster.on('exit', function (worker, code, signal) {
    console.warn(
      `[${worker.id}] Worker died : [PID ${worker.process.pid}] [Signal ${signal}] [Code ${code}]`
    );
    cluster.fork();
  });
} else {
  console.log(
    `[${cluster.worker.id}] [PID ${cluster.worker.process.pid}] Worker`
  );

  // Workers share the TCP connection in this server
  const app = express();

  app.use(cors({ origin: 'http://localhost:8000' }));

  // parse requests of content-type - application/json
  app.use(express.json());

  // parse requests of content-type - application/x-www-form-urlencoded
  // app.use(express.urlencoded({ extended: true }));

  app.use((req, res, next) => {
    // checkCustomHeader
    if (req.method !== 'OPTIONS' && !req.header('X-Requested-With')) {
      res.status(400);
      res.send({ result: 'error' });
      res.end();
      return;
    }

    res.header(
      'Access-Control-Allow-Headers',
      'Origin, X-Requested-With, Content-Type, Accept'
    );
    res.header('Access-Control-Allow-Methods', 'POST, OPTIONS');
    // res.header('Access-Control-Allow-Credentials', true);
    res.header('Access-Control-Max-Age', '600');
    next();
  });

  app.options('*', (req, res) => {
    res.sendStatus(200);
  });

  app.use('/api/search', SearchController);

  app.listen(process.env.PORT || 8080, () =>
    logger.system.info('Server is running.')
  );
}
