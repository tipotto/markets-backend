const SearchController = require('../controllers/search.controller.js');
const router = require('express').Router();

module.exports = (app) => {
  router.post('/', SearchController);
  app.use('/api/search', router);
};
