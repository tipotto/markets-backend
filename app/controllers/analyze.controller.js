const AnalyzeService = require('../services/analyze.service');
const httpLogger = require('../config/log4js.config').http;
const { validationResult } = require('express-validator');
const PyShellError = require('../exceptions/PyShellError');
const ParseError = require('../exceptions/ParseError');

module.exports = (req, res) => {
  // const errors = validationResult(req);
  // if (!errors.isEmpty()) {
  //   res.status(422).json({ error: 'The request is invalid.' });
  //   httpLogger.error(errors);
  //   return;
  // }

  // let { body } = req;
  // const { platforms, deliveryCost } = body;

  // if (deliveryCost === 'required' && platforms.includes('paypay')) {
  //   const removed = platforms.filter((p) => p !== 'paypay');
  //   // console.log('platforms', removed);

  //   if (!removed.length) {
  //     // console.log('Platforms array is empty.');
  //     res.status(200).json([]);
  //     httpLogger.info('All processes are successfully completed.');
  //     return;
  //   }

  //   body.platforms = removed;
  // }

  // console.log('form', body);

  AnalyzeService.init()
    .analyze(req.body)
    // .search(body)
    .then(({ status, results, error }) => {
      res.status(200).json(results);

      if (status === 'success') {
        httpLogger.info('All processes are successfully completed.');
      } else {
        httpLogger.error(error);
      }
    })
    .catch((e) => {
      if (e instanceof ParseError) {
        res.status(502).json({ error: 'Bad Gateway' });
      } else if (e instanceof PyShellError) {
        res.status(500).json({ error: 'Internal Server Error' });
      }
      httpLogger.error(e);
    });
};
