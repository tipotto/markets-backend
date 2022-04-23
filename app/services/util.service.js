/* eslint-disable node/no-unsupported-features */
import { GoogleAuth } from 'google-auth-library';
import axios from 'axios';
import { validationResult } from 'express-validator';
import { PythonShell, PythonShellError } from 'python-shell';
import { http as httpLogger } from '../config/log4js.config.js';
import RequestError from '../exceptions/RequestError.js';
import ParseError from '../exceptions/ParseError.js';
import NotificationError from '../exceptions/NotificationError.js';

export const handleRequest = (req, res, type, func) => {
  checkValidationResult(req)
    .then(func)
    .then(({ status, result, error }) => {
      res.status(200).json(getResJson(null, result));
      httpLogger.info('All processes are successfully completed.');
    })
    .catch(async (e) => {
      responseError(res, e);
      const traceback = moldError(e);
      httpLogger.error(traceback);
      return await notifyError(type, req.body, traceback);
    })
    .then((message) => {
      if (!message) return;
      httpLogger.info(message);
    })
    .catch((e) => {
      httpLogger.error(moldError(e));
    });
};

export const scrape = (form, pyScriptPath, func) => {
  return new Promise((resolve, reject) => {
    try {
      const shell = new PythonShell(pyScriptPath, {
        mode: 'json',
      });

      shell.send(form);
      shell.on('message', (data) => {
        try {
          resolve(func(form, data));
        } catch (e) {
          reject(new ParseError(e));
        }
      });

      shell.end((err, code, signal) => {
        try {
          if (err) throw err;
        } catch (e) {
          reject(e);
        }
      });
    } catch (e) {
      reject(e);
    }
  });
};

export const moldError = (err) => {
  return err.traceback || err.message || err;
};

export const fetchGoogleAuthToken = async () => {
  const auth = new GoogleAuth();
  const client = await auth.getIdTokenClient(
    process.env.SLACK_ERROR_NOTIFICATION_URL,
  );
  const idToken = await client.idTokenProvider.fetchIdToken(
    process.env.SLACK_ERROR_NOTIFICATION_URL,
  );

  return idToken;
};

export const notifyError = async (type, form, err) => {
  const idToken = await fetchGoogleAuthToken();
  const options = {
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'axios',
      'X-Requested-By': 'markets.jp',
      Authorization: `bearer ${idToken}`,
    },
  };

  const params = {
    type,
    form,
    error: typeof err === 'object' ? JSON.stringify(err) : err,
  };

  const {
    status,
    data: { message, error },
  } = await axios.post(
    process.env.SLACK_ERROR_NOTIFICATION_URL,
    JSON.stringify(params),
    options,
  );

  if (status !== 200) {
    throw new NotificationError(error);
  }

  return message;
};

export const checkValidationResult = async (req) => {
  const error = validationResult(req);
  if (!error.isEmpty()) {
    throw new RequestError(`The request is invalid.\n${error}`);
  }
  return req.body;
};

export const getResJson = (errMessage, result = null) => {
  const resJson = { result: null, error: null };
  if (result) {
    return { ...resJson, result };
  }
  return { ...resJson, error: errMessage };
};

export const responseError = (res, error) => {
  if (error instanceof RequestError) {
    res.status(400).json(getResJson('Bad Request'));
  } else if (error instanceof ParseError) {
    res.status(502).json(getResJson('Bad Gateway'));
  } else if (error instanceof PythonShellError) {
    res.status(500).json(getResJson('Internal Server Error'));
  } else if (error instanceof NotificationError) {
    res.status(502).json(getResJson('Bad Gateway'));
  }
};

const sortInAscOrder = (arr) => {
  return arr.sort((a, b) => (a.price.int < b.price.int ? -1 : 1));
};

const sortInDescOrder = (arr) => {
  return arr.sort((a, b) => (a.price.int > b.price.int ? -1 : 1));
};

export const sortArray = (arr, sortOrder) => {
  if (!arr.length) return [];
  if (sortOrder === 'asc') {
    return sortInAscOrder(arr);
  }
  return sortInDescOrder(arr);
};

export const moldArray = (arr) => {
  if (!arr.length) {
    return { byId: {}, allIds: [] };
  }

  const byId = {};
  const allIds = arr.map((item) => {
    byId[item.id] = item;
    return item.id;
  });

  return { byId, allIds };
};
