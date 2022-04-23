/* eslint-disable node/no-unsupported-features */
import { scrape, sortArray, moldArray } from './util.service.js';

const moldItems = ({ sortOrder }, data) => {
  const {
    result: { items, pages },
  } = data;

  const sorted = sortArray(items, sortOrder);
  const { byId, allIds } = moldArray(sorted);

  data.result = {
    items: { byId, allIds },
    pages,
  };

  return data;
};

const getSearchScriptPath = () => {
  if (process.env.NODE_ENV === 'development') {
    return process.env.DEV_PYTHON_SEARCH_SCRIPT;
  }
  return process.env.PROD_PYTHON_SEARCH_SCRIPT;
};

const search = async (form) => {
  return scrape(form, getSearchScriptPath(), moldItems);
};

export default search;
