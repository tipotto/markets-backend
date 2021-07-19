const { PythonShell } = require('python-shell');
const BaseService = require('./base.service');

module.exports = class SearchService extends BaseService {
  constructor() {
    super();
    if (process.env.NODE_ENV === 'development') {
      this.pyScriptPath = process.env.DEV_PYTHON_SEARCH_SCRIPT;
    } else {
      this.pyScriptPath = process.env.PROD_PYTHON_SEARCH_SCRIPT;
    }
  }

  static init() {
    return new SearchService();
  }

  ravelArray(arr) {
    if (!arr.length) {
      return { items: [], pages: [0] };
    }

    let items = [];
    const pages = arr.map((obj) => {
      items = [...items, ...obj.items];
      return obj.pages;
    });
    return { items, pages };
  }

  getAryMax(a, b) {
    return Math.max(a, b);
  }

  moldItems({ type, sortOrder }, { result }) {
    const { items, pages } = this.ravelArray(result);
    const sorted = super.sortArray(items, sortOrder);
    const { byId, allIds } = super.moldArray(sorted);

    const maxPage = type === 'next' ? 0 : pages.reduce(this.getAryMax);

    return {
      items: { byId, allIds },
      pages: maxPage,
    };
  }

  scrape(form) {
    return new Promise((resolve, reject) => {
      // console.log('1. python-shellの呼び出し。');

      const start_ms = new Date().getTime();
      // console.log('start time', start_ms);

      const shell = new PythonShell(this.pyScriptPath, {
        mode: 'json',
      });

      // console.log('2. フォームデータをpython側に送信。');
      shell.send(form);

      shell.on('message', async (data) => {
        try {
          // console.log('3. データを取得');
          data.result = this.moldItems(form, data);
          resolve(data);
        } catch (e) {
          // console.log('JSON parse error:', e);
          reject(e);
        }
      });

      shell.end((err, code, signal) => {
        if (err) {
          // この時点でのエラーにはPythonのトレースバックも含まれるが、
          // コントローラー側でログに出力する際に削除される。
          // console.log('Python Shell error', err);
          reject(err);
        }
        // console.log('4. 一通り処理を終了。');

        const elapsed_ms = new Date().getTime() - start_ms;
        // console.log('end time', elapsed_ms);
      });
    });
  }

  async search(form) {
    return this.scrape(form);
  }
};
