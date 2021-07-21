const { PythonShell } = require('python-shell');
const base = require('./base.service');

const moldItems = ({ sortOrder }, { result: { items, pages } }) => {
  const sorted = base.sortArray(items, sortOrder);
  const { byId, allIds } = base.moldArray(sorted);

  return {
    items: { byId, allIds },
    pages: pages,
  };
};

const scrape = (form) => {
  return new Promise((resolve, reject) => {
    // console.log('1. python-shellの呼び出し。');

    // const start_ms = new Date().getTime();
    // console.log('start time', start_ms);

    let pyScriptPath = null;
    if (process.env.NODE_ENV === 'development') {
      pyScriptPath = process.env.DEV_PYTHON_SEARCH_SCRIPT;
    } else {
      pyScriptPath = process.env.PROD_PYTHON_SEARCH_SCRIPT;
    }

    const shell = new PythonShell(pyScriptPath, {
      mode: 'json',
    });

    // console.log('2. フォームデータをpython側に送信。');
    shell.send(form);

    shell.on('message', async (data) => {
      try {
        // console.log('3. データを取得');
        data.result = moldItems(form, data);
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

      // const elapsed_ms = new Date().getTime() - start_ms;
      // console.log('end time', elapsed_ms);
    });
  });
};

const search = async (form) => {
  return scrape(form);
};

module.exports = { search };
