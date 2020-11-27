const express = require('express');
// const log4js = require('log4js');
const cors = require('cors');
const app = express();
// const db = require('./app/models/');
const logger = require('./app/config/log4js.config.js');
// const cron = require('node-cron');
const SearchRoute = require('./app/routes/search.routes');

var corsOptions = {
  origin: 'http://localhost:8000',
};

app.use(cors(corsOptions));

// parse requests of content-type - application/json
app.use(express.json());

// parse requests of content-type - application/x-www-form-urlencoded
app.use(express.urlencoded({ extended: true }));

// db.sequelize.sync();
// db.sequelize.sync({ force: true }).then(() => {
//   console.log('Drop and re-sync db.');
// });

// 毎日0時にキャッシュを削除
// cron.schedule('0 0 0 * * *', () => {
//   SearchService.deleteAll()
//     .then((value) => {
//       console.log('削除処理が完了しました。');
//     })
//     .catch((err) => {
//       console.log('エラーが発生しました: ' + err.message);
//     });
// });

// ログ設定
// log4js.configure("./app/config/log4js.config.json");
// const systemLogger = log4js.getLogger("system");
// const httpLogger = log4js.getLogger("http");
// const accessLogger = log4js.getLogger("access");
// app.use(log4js.connectLogger(accessLogger));
// app.use(log4js.connectLogger(logger.access));
app.use((req, res, next) => {
  if (
    typeof req === 'undefined' ||
    req === null ||
    typeof req.method === 'undefined' ||
    req.method === null ||
    typeof req.header === 'undefined' ||
    req.header === null
  ) {
    next();
    return;
  }

  // if (req.method === "GET" || req.method === "DELETE") {
  //   httpLogger.info(req.query);
  // } else {
  //   httpLogger.info(req.body);
  // }
  if (req.method === 'POST') {
    logger.http.info(req.body);
  }
  next();
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () =>
  logger.system.info(`App has been started. Server is running on port ${PORT}.`)
);

SearchRoute(app);
