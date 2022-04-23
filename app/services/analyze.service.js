/* eslint-disable node/no-unsupported-features */
import { scrape, sortArray, moldArray } from './util.service.js';

const moldItems = ({ sortOrder }, data) => {
  const {
    items: { all, market },
  } = data.result;

  const sortedAll = sortArray(all.list, sortOrder);
  const sortedMarket = sortArray(market.list, sortOrder);
  const moldedAll = moldArray(sortedAll);
  const moldedMarket = moldArray(sortedMarket);

  const allItems = {
    list: sortedAll,
    byId: moldedAll.byId,
    allIds: moldedAll.allIds,
  };

  const marketItems = {
    list: sortedMarket,
    byId: moldedMarket.byId,
    allIds: moldedMarket.allIds,
  };

  data.result.items = {
    all: allItems,
    market: marketItems,
  };

  return data;
};

const getAnalyzeScriptPath = () => {
  if (process.env.NODE_ENV === 'development') {
    return process.env.DEV_PYTHON_ANALYZE_SCRIPT;
  }
  return process.env.PROD_PYTHON_ANALYZE_SCRIPT;
};

const analyze = async (form) => {
  return scrape(form, getAnalyzeScriptPath(), moldItems);
};

export default analyze;
