const { PythonShell } = require('python-shell');
const BaseService = require('./base.service');

module.exports = class AnalyzeService extends BaseService {
  constructor() {
    super();
    if (process.env.NODE_ENV === 'development') {
      this.pyScriptPath = process.env.DEV_PYTHON_ANALYZE_SCRIPT;
    } else {
      this.pyScriptPath = process.env.PROD_PYTHON_ANALYZE_SCRIPT;
    }
  }

  static init() {
    return new AnalyzeService();
  }

  moldItems({ sortOrder }, { items: { all, market } }) {
    // アイテムのソート
    const sortedAll = super.sortArray(all.list, sortOrder);
    const sortedMarket = super.sortArray(market.list, sortOrder);

    // アイテムの成形
    const moldedAll = super.moldArray(sortedAll);
    const moldedMarket = super.moldArray(sortedMarket);

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

    return {
      all: allItems,
      market: marketItems,
    };
  }

  scrape(form) {
    return new Promise((resolve, reject) => {
      // console.log('1. python-shellの呼び出し');

      // const start_ms = new Date().getTime();
      // console.log('start time', start_ms);

      const shell = new PythonShell(this.pyScriptPath, {
        mode: 'json',
      });

      // console.log('2. フォームデータをpython側に送信');
      shell.send(form);

      shell.on('message', async (data) => {
        try {
          // console.log('3. データを取得');
          data.result.items = this.moldItems(form, data.result);
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
          // console.log('The exit code was: ' + code);
          // console.log('The exit signal was: ' + signal);
          reject(err);
        }
        // console.log('4. 一通り処理を終了');

        // const elapsed_ms = new Date().getTime() - start_ms;
        // console.log('end time', elapsed_ms);
      });
    });
  }

  async analyze(form) {
    return this.scrape(form);
  }
};
