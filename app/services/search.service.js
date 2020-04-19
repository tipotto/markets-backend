const db = require("../models/index");
const Search = db.search;
const Key = require("../constants/user");
const pyPath = require("../constants/search");
var { PythonShell } = require("python-shell");

module.exports = class SearchService {
  /**
   * コンストラクタ
   * @param {*} res
   */
  constructor(res) {
    this.res = res;
  }

  /**
   * 初期化
   * @param {*} res
   */
  static init(res) {
    return new SearchService(res);
  }

  /**
   * 配列の登録
   * @param {*} resultArray
   */
  bulkCreate(resultArray) {
    const promiseArray = [];

    resultArray.forEach((result) => {
      const promise = new Promise((resolve, reject) => {
        Search.bulkCreate(result)
          .then((items) => {
            resolve(items);
          })
          .catch((err) => {
            reject(err);
          });
      });
      promiseArray.push(promise);
    });

    return promiseArray;
  }

  // bulkCreate(searchResultArray) {
  //   return new Promise((resolve, reject) => {
  //     Search.bulkCreate(searchResultArray)
  //       .then((items) => {
  //         resolve(items);
  //       })
  //       .catch((err) => {
  //         reject(err);
  //       });
  //   });
  // }

  /**
   * アイテムリストの取得
   * @param {*} form
   */
  findAll(form) {
    return new Promise((resolve, reject) => {
      Search.findAll({
        limit: form.resultNum,
        order: [[form.sortIndex, form.sortOrder]],
        // where: {}
      })
        .then((items) => {
          resolve(items);
        })
        .catch((err) => {
          reject(err);
        });
    });
  }

  /**
   * アイテムリストを全削除
   */
  deleteAll() {
    return new Promise((resolve, reject) => {
      Search.destroy({
        where: {},
        truncate: false,
      })
        .then((items) => {
          resolve();
        })
        .catch((err) => {
          reject(err);
        });
    });
  }

  /**
   * 検索
   * @param {*} form
   */
  search(form) {
    return new Promise((resolve, reject) => {
      console.log("1. python-shellの呼び出し。");
      var pyshell = new PythonShell(pyPath, {
        mode: "text",
      });

      var json = {
        pfArray: form.pfArray,
        keyword: form.keyword,
      };

      console.log("2. フォームデータをpython側に送信。");
      pyshell.send(JSON.stringify(json));

      pyshell.on("message", (data) => {
        console.log("3. スクレイピング結果の取得。");
        console.log("検索結果： " + data);

        const resultArray = JSON.parse(data || "null");
        Promise.all(this.bulkCreate(resultArray)).then((items) => {
          console.log("4. 検索結果を登録完了。");
          this.findAll(form)
            .then((items) => {
              console.log("5. 検索結果を取得完了。");
              this.res.status(Key.FETCH.SUCCESS.httpResCode).send(items);
              this.deleteAll();
            })
            .then((items) => {
              console.log("6. 検索結果を削除完了。");
            })
            .catch((err) => {
              reject(err);
            });
        });
      });

      pyshell.end((err) => {
        if (err) reject(err);
        console.log("7. 一通り処理を終了。");
        resolve("スクレイピング完了。");
      });
    });
  }

  // search(form) {
  //   return new Promise((resolve, reject) => {
  //     console.log("python-shellの呼び出し(node: searchService)");
  //     var pyshell = new PythonShell(pyPath, {
  //       mode: "text",
  //     });

  //     var json = {
  //       pfArray: form.pfArray,
  //       keyword: form.keyword,
  //     };

  //     console.log("jsonをpython側に送信(node: searchService)");
  //     pyshell.send(JSON.stringify(json));

  //     var promiseArray = [];
  //     pyshell.on("message", (data) => {
  //       console.log("mercari： " + data);
  //       this.bulkCreate(JSON.parse(data || "null"))
  //         .then((items) => {
  //           promiseArray.push(items);
  //           console.log(
  //             "検索結果を登録し、promiseオブジェクトをプッシュしました。(node: searchService onメソッド)"
  //           );
  //         })
  //         .catch((err) => {
  //           console.log(err.message);
  //         });
  //     });

  //     pyshell.end((err) => {
  //       Promise.all(promiseArray).then((data) => {
  //         this.findAll(form.resultNum, form.sortIndex, form.sortOrder)
  //           .then((items) => {
  //             this.res.status(Key.FETCH.SUCCESS.httpResCode).send(items);
  //             this.deleteAll();
  //           })
  //           .then((items) => {
  //             console.log("end");
  //             resolve("mercari finished.");
  //           })
  //           .catch((err) => {
  //             reject(err);
  //           });
  //       });
  //     });
  //   });
  // }
};
