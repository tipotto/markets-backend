/* eslint-disable node/no-unsupported-features */
import cluster from 'cluster';
import express from 'express';
import log4js from 'log4js';
import { cpus } from 'os';
import { config } from 'dotenv';
import {
  system as systemLogger,
  access as accessLogger,
} from './app/config/log4js.config.js';
import accessController from './app/controllers/access.controller.js';
import authorizeController from './app/controllers/authorize.controller.js';
import searchRequestController from './app/controllers/search.request.controller.js';
import searchValidator from './app/validates/search.validate.js';
import searchController from './app/controllers/search.controller.js';
import analyzeRequestController from './app/controllers/analyze.request.controller.js';
import analyzeValidator from './app/validates/analyze.validate.js';
import analyzeController from './app/controllers/analyze.controller.js';
import { moldError } from './app/services/util.service.js';

try {
  // クラスタリング
  if (cluster.isMaster) {
    for (var i = 0; i < cpus().length; i++) {
      systemLogger.info(`Master : Cluster Fork ${i}`);
      // Create a worker process
      cluster.fork();
    }

    // Workers share the TCP connection in this server
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

    // loads .env file into process.env
    config();

    const app = express();
    app.disable('x-powered-by');

    // parse requests of content-type - application/json
    app.use(express.json());

    // Expressへのアクセスログを出力
    app.use(log4js.connectLogger(accessLogger));
    app.use(accessController);

    // 正規のクライアント（markets.jpのブラウザページ）からのアクセスの場合、
    // CORS回避のためにAPI（http://localhost:8080）をプロキシとして利用しているため、
    // Same-Originによりプリフライトリクエストが実行されない。
    // しかし、悪意あるユーザーによる外部からのブラウザアクセスに備えて残しておく。
    // app.options("*", authorizeController);
    app.post('/api/v1/*', authorizeController);

    app.post(
      '/api/v1/search',
      searchRequestController,
      searchValidator,
      searchController,
    );

    app.post(
      '/api/v1/analyze',
      analyzeRequestController,
      analyzeValidator,
      analyzeController,
    );

    const port = process.env.PORT || 8080;
    app.listen(port, () =>
      systemLogger.info(`Server is running on port ${port}.`),
    );
  }
} catch (e) {
  systemLogger.error(
    `Failed to start server on port ${process.env.PORT || 8080}.\n${moldError(
      e,
    )}`,
  );
}
