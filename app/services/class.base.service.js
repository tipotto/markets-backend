module.exports = class BaseService {
  // サブクラスのコンストラクタ内でsuperを呼び出す必要あり
  // そうしないとエラーになり、それ以降のthisを使ったプロパティアクセスもできない
  // そのため、空のコンストラクタを定義
  constructor() {}

  sortInAscOrder(arr) {
    return arr.sort((a, b) => (a.price.int < b.price.int ? -1 : 1));
  }

  sortInDescOrder(arr) {
    return arr.sort((a, b) => (a.price.int > b.price.int ? -1 : 1));
  }

  sortArray(arr, sortOrder) {
    // console.log('3. 検索結果をソート。');
    if (!arr.length) return [];

    if (sortOrder === 'asc') {
      return this.sortInAscOrder(arr);
    }
    return this.sortInDescOrder(arr);
  }

  moldArray(arr) {
    if (!arr.length) {
      return { byId: {}, allIds: [] };
    }

    const byId = {};
    const allIds = arr.map((item) => {
      byId[item.id] = item;
      return item.id;
    });
    return { byId, allIds };
  }
};
