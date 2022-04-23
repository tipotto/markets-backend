/* eslint-disable node/no-unsupported-features */
import { access as accessLogger } from '../config/log4js.config.js';

const accessController = (req, res, next) => {
  if (!req || !req.method || !req.headers) {
    // next();
    // accessLogger.error("The request doesn't have necessary parameters.");
    return;
  }

  if (req.method === 'GET' || req.method === 'DELETE') {
    accessLogger.info(req.query);
  } else {
    accessLogger.info(req.body);
  }
  next();
};

export default accessController;
