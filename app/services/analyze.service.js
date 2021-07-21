const { PythonShell } = require('python-shell');
const base = require('./base.service');

const moldItems = ({ sortOrder }, { items: { all, market } }) => {
  // アイテムのソート
  const sortedAll = base.sortArray(all.list, sortOrder);
  const sortedMarket = base.sortArray(market.list, sortOrder);

  // アイテムの成形
  const moldedAll = base.moldArray(sortedAll);
  const moldedMarket = base.moldArray(sortedMarket);

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
};

const scrape = (form) => {
  return new Promise((resolve, reject) => {
    // console.log('1. python-shellの呼び出し');

    // const start_ms = new Date().getTime();
    // console.log('start time', start_ms);

    let pyScriptPath = null;
    if (process.env.NODE_ENV === 'development') {
      pyScriptPath = process.env.DEV_PYTHON_ANALYZE_SCRIPT;
    } else {
      pyScriptPath = process.env.PROD_PYTHON_ANALYZE_SCRIPT;
    }

    const shell = new PythonShell(pyScriptPath, {
      mode: 'json',
    });

    // console.log('2. フォームデータをpython側に送信');
    shell.send(form);

    shell.on('message', async (data) => {
      try {
        // console.log('3. データを取得');
        data.result.items = moldItems(form, data.result);
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
      // console.log('4. 一通り処理を終了');

      // const elapsed_ms = new Date().getTime() - start_ms;
      // console.log('end time', elapsed_ms);
    });
  });
};

const analyze = async (form) => {
  return scrape(form);
};

module.exports = { analyze };
