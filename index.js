const cluster = require('cluster');
const express = require('express');
const log4js = require('log4js');
const numCPUs = require('os').cpus().length;
const logger = require('./app/config/log4js.config.js');
const systemLogger = logger.system;
const accessLogger = logger.access;
const AccessController = require('./app/controllers/access.controller');
const AuthorizeController = require('./app/controllers/authorize.controller');
const RequestController = require('./app/controllers/request.controller');
const RequestValidator = require('./app/validates/request.validate');
const SearchController = require('./app/controllers/search.controller.js');

require('dotenv').config();
const port = process.env.PORT || 8080;

// クラスタリング
if (cluster.isMaster) {
  for (var i = 0; i < numCPUs; i++) {
    systemLogger.info(`Master : Cluster Fork ${i}`);
    // Create a worker process
    cluster.fork();
  }

  cluster.on('exit', function (worker, code, signal) {
    systemLogger.warn(
      `[${worker.id}] Worker died : [PID ${worker.process.pid}] [Signal ${signal}] [Code ${code}]`,
    );
    cluster.fork();
  });
} else {
  systemLogger.info(
    `[${cluster.worker.id}] [PID ${cluster.worker.process.pid}] Worker`,
  );
  // Workers share the TCP connection in this server
  const app = express();
  app.disable('x-powered-by');

  // parse requests of content-type - application/json
  app.use(express.json());

  // Expressへのアクセスログを出力
  app.use(log4js.connectLogger(accessLogger));
  app.use(AccessController);

  // 正規のクライアント（markets.jpのブラウザページ）からのアクセスの場合、
  // CORS回避のためにAPI（http://localhost:8080）をプロキシとして利用しているため、
  // Same-Originによりプリフライトリクエストが実行されない。
  // しかし、悪意あるユーザーによる外部からのブラウザアクセスに備えて残しておく。
  // app.options("*", AuthorizeController);

  app.post('/api/v1/search', AuthorizeController);

  app.post(
    '/api/v1/search',
    RequestController,
    RequestValidator,
    SearchController,
  );

  app.listen(port, () =>
    systemLogger.info(`Server is running on port ${port}.`),
  );
}
