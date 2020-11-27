const Key = require('../constants/search');
const { PythonShell } = require('python-shell');

module.exports = class SearchService {
  static init() {
    return new SearchService();
  }

  sortInAscOrder(data) {
    return data.sort((a, b) => (a.price < b.price ? -1 : 1));
  }

  sortInDescOrder(data) {
    return data.sort((a, b) => (a.price > b.price ? -1 : 1));
  }

  sortArray(data, sortOrder) {
    console.log('4. 検索結果をソート。');
    if (sortOrder === 'ASC') {
      return this.sortInAscOrder(data);
    }
    return this.sortInDescOrder(data);
  }

  integrateArray(resultArr) {
    console.log('3. 検索結果の配列をマージ。');

    let results = [];
    resultArr.forEach((arr) => {
      results = [...results, ...arr];
    });
    return results;
  }

  scrape({ query, platforms, sortOrder }) {
    return new Promise((resolve, reject) => {
      console.log('1. python-shellの呼び出し。');

      const pyShell = new PythonShell(Key.PYTHON_PATH, {
        mode: 'text',
      });

      console.log('2. フォームデータをpython側に送信。');
      pyShell.send(JSON.stringify({ query, platforms }));

      pyShell.on('message', async (data) => {
        const results = JSON.parse(data || 'null');
        const integrated = this.integrateArray(results);
        const sorted = this.sortArray(integrated, sortOrder);
        resolve(sorted);
      });

      pyShell.end((err) => {
        if (err) reject(err);
        console.log('5. 一通り処理を終了。');
      });
    });
  }

  async search(form) {
    return this.scrape(form);
  }
};
