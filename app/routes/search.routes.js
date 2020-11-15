const SearchController = require('../controllers/search.controller.js');
const express = require('express');

module.exports = (app) => {
  var router = express.Router();
  router.post('/', SearchController);
  app.use('/api/search', router);
};
