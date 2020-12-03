const express = require('express');
const cors = require('cors');
const app = express();
const logger = require('./app/config/log4js.config.js');
const SearchController = require('./app/controllers/search.controller.js');

var corsOptions = {
  origin: 'http://localhost:8000',
};

app.use(cors(corsOptions));

// parse requests of content-type - application/json
app.use(express.json());

// parse requests of content-type - application/x-www-form-urlencoded
app.use(express.urlencoded({ extended: true }));

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
  // GETは必要ない可能性が高い
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
