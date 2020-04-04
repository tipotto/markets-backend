const express = require("express");
const log4js = require("log4js");
const mysql = require("mysql");
const cors = require("cors");
const app = express();
const db = require("./app/models/");
const logger = require("./app/config/log4js.config.js");

var corsOptions = {
  origin: "http://localhost:8000"
};

app.use(cors(corsOptions));

// parse requests of content-type - application/json
app.use(express.json());

// parse requests of content-type - application/x-www-form-urlencoded
app.use(express.urlencoded({ extended: true }));

// db.sequelize.sync();
db.sequelize.sync({ force: true }).then(() => {
  console.log("Drop and re-sync db.");
});

// const client =
//   process.env.NODE_ENV === "production"
//     ? mysql.createConnection({
//         user: process.env.REACT_APP_DB_USER,
//         password: process.env.REACT_APP_DB_PASSWORD,
//         database: process.env.REACT_APP_DB_DATABASE,
//         socketPath: `/cloudsql/${process.env.REACT_APP_INSTANCE_CONNECTION_NAME}`
//       })
//     : mysql.createConnection({
//         user: process.env.REACT_APP_DB_USER,
//         password: process.env.REACT_APP_DB_PASSWORD,
//         database: process.env.REACT_APP_DB_DATABASE,
//         host: "localhost"
//       });

// ログ設定
// log4js.configure("./app/config/log4js.config.json");
// const systemLogger = log4js.getLogger("system");
// const httpLogger = log4js.getLogger("http");
// const accessLogger = log4js.getLogger("access");
// app.use(log4js.connectLogger(accessLogger));
app.use(log4js.connectLogger(logger.access));
app.use((req, res, next) => {
  if (
    typeof req === "undefined" ||
    req === null ||
    typeof req.method === "undefined" ||
    req.method === null ||
    typeof req.header === "undefined" ||
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
  if (req.method === "POST") {
    logger.http.info(req.body);
  }
  next();
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () =>
  logger.system.info(`App has been started. Server is running on port ${PORT}.`)
);

require("./app/routes/search.routes")(app);
// require("./app/routes/user.routes")(app);
// TODO item.serviceの内容確認、itemのconstantsの作成などが未完了。
// require("./app/routes/item.routes")(app);
