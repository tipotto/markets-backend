const sortInAscOrder = (arr) => {
  return arr.sort((a, b) => (a.price.int < b.price.int ? -1 : 1));
};

const sortInDescOrder = (arr) => {
  return arr.sort((a, b) => (a.price.int > b.price.int ? -1 : 1));
};

const sortArray = (arr, sortOrder) => {
  if (!arr.length) return [];

  if (sortOrder === 'asc') {
    return sortInAscOrder(arr);
  }
  return sortInDescOrder(arr);
};

const moldArray = (arr) => {
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

module.exports = { sortArray, moldArray };
