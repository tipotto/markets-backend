const { PythonShell } = require("python-shell");
const PyShellError = require("../exceptions/PyShellError");
const ParseError = require("../exceptions/ParseError");

module.exports = class SearchService {
  constructor() {
    if (process.env.NODE_ENV === "development") {
      return (this.pyScriptPath = process.env.DEV_PYTHON_SCRIPT);
    }
    this.pyScriptPath = process.env.PROD_PYTHON_SCRIPT;
  }

  static init() {
    return new SearchService();
  }

  sortInAscOrder(arr) {
    return arr.sort((a, b) => (a.price.int < b.price.int ? -1 : 1));
  }

  sortInDescOrder(arr) {
    return arr.sort((a, b) => (a.price.int > b.price.int ? -1 : 1));
  }

  sortArray(arr, sortOrder) {
    console.log("3. 検索結果をソート。");
    if (!arr.length) return arr;

    if (sortOrder === "asc") {
      return this.sortInAscOrder(arr);
    }
    return this.sortInDescOrder(arr);
  }

  // integrateArray(resultArr) {
  //   console.log('3. 検索結果の配列をマージ。');

  //   let results = [];
  //   resultArr.forEach((arr) => {
  //     results = [...results, ...arr];
  //   });
  //   return results;
  // }

  scrape(form) {
    return new Promise((resolve, reject) => {
      console.log("pyScriptPath", this.pyScriptPath);
      console.log("1. python-shellの呼び出し。");
      const pyShell = new PythonShell(this.pyScriptPath, {
        mode: "text",
      });

      console.log("2. フォームデータをpython側に送信。");
      pyShell.send(JSON.stringify(form));

      pyShell.on("message", async (data) => {
        try {
          let parsed = JSON.parse(data || "null");
          console.log("result", parsed);

          // Scrapyの場合
          // resultsには配列が返ってくる
          // const sorted = this.sortArray(results, form.sortOrder);

          // Asyncioの場合
          // resultsには多次元配列が返ってくる
          // そのため、1つの配列にまとめる必要あり
          // const integrated = this.integrateArray(results);
          // const sorted = this.sortArray(integrated, form.sortOrder);

          const sorted = this.sortArray(parsed.results, form.sortOrder);
          parsed.results = sorted;
          resolve(parsed);
        } catch (e) {
          console.log("JSON parse error:", e);
          reject(new ParseError(e));
        }
      });

      pyShell.end((e) => {
        if (e) {
          // この時点でのエラーにはPythonのトレースバックも含まれるが、
          // コントローラー側でログに出力する際に削除される。
          console.log("Python Shell error", e);
          reject(new PyShellError(e));
        }
        console.log("4. 一通り処理を終了。");
      });
    });
  }

  async search(form) {
    return this.scrape(form);
  }
};
