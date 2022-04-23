/* eslint-disable node/no-unsupported-features */
import analyze from '../services/analyze.service.js';
import { handleRequest } from '../services/util.service.js';

const analyzeController = (req, res, next) => {
  handleRequest(req, res, 'analyze', analyze);
};

export default analyzeController;
