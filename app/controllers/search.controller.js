const SearchService = require('../services/search.service');
const httpLogger = require('../config/log4js.config').http;
const { validationResult } = require('express-validator');
const PyShellError = require('../exceptions/PyShellError');
const ParseError = require('../exceptions/ParseError');

module.exports = (req, res) => {
  // return res.status(422).json({ error: "The request data is invalid." });

  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    res.status(422).json({ error: 'The request is invalid.' });
    httpLogger.error(errors);
    return;
  }

  let { body } = req;
  const { platforms, deliveryCost } = body;

  if (deliveryCost === 'required' && platforms.includes('paypay')) {
    const removed = platforms.filter((p) => p !== 'paypay');
    // console.log('platforms', removed);

    if (!removed.length) {
      // console.log('Platforms array is empty.');
      res.status(200).json([]);
      httpLogger.info('All processes are successfully completed.');
      return;
    }

    body.platforms = removed;
  }

  // console.log('form', body);

  SearchService.init()
    .search(body)
    .then(({ status, result, error }) => {
      // console.log('result', result);
      res.status(200).json(result);

      if (status === 'success') {
        httpLogger.info('All processes are successfully completed.');
      } else {
        httpLogger.error(error);
      }
    })
    .catch((e) => {
      // if (e instanceof ParseError) {
      //   res.status(502).json({ error: 'Bad Gateway' });
      // } else if (e instanceof PyShellError) {
      //   res.status(500).json({ error: 'Internal Server Error' });
      // }
      res.status(500).json({ error: 'Internal Server Error' });
      httpLogger.error(e);
    });
};
