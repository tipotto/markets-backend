/* eslint-disable node/no-unsupported-features */
import search from '../services/search.service.js';
import { handleRequest } from '../services/util.service.js';

const searchController = (req, res, next) => {
  handleRequest(req, res, 'search', search);
};

export default searchController;
