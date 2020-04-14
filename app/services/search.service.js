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
   * @param {*} searchResultArray
   */
  bulkCreate(searchResultArray) {
    return new Promise((resolve, reject) => {
      Search.bulkCreate(searchResultArray)
        .then((items) => {
          resolve(items);
        })
        .catch((err) => {
          reject(err);
        });
    });
  }

  /**
   * アイテムリストの取得
   * @param {*} resultNum
   * @param {*} sortIndex
   * @param {*} sortOrder
   */
  findAll(resultNum, sortIndex, sortOrder) {
    return new Promise((resolve, reject) => {
      Search.findAll({
        limit: resultNum,
        order: [[sortIndex, sortOrder]],
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
        .then(() => {
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
      console.log("python-shellの呼び出し(node: searchService)");
      var pyshell = new PythonShell(pyPath, {
        mode: "text",
      });

      var json = {
        pfArray: form.pfArray,
        keyword: form.keyword,
      };

      console.log("jsonをpython側に送信(node: searchService)");
      pyshell.send(JSON.stringify(json));

      var promiseArray = [];
      pyshell.on("message", (data) => {
        console.log("mercari： " + data);
        this.bulkCreate(JSON.parse(data || "null"))
          .then((items) => {
            promiseArray.push(items);
            console.log(
              "検索結果を登録し、promiseオブジェクトをプッシュしました。(node: searchService onメソッド)"
            );
          })
          .catch((err) => {
            console.log(err.message);
          });
      });

      pyshell.end((err) => {
        Promise.all(promiseArray).then((data) => {
          this.findAll(form.resultNum, form.sortIndex, form.sortOrder)
            .then((items) => {
              this.res.status(Key.FETCH.SUCCESS.httpResCode).send(items);
              this.deleteAll();
            })
            .then((items) => {
              console.log("end");
              resolve("mercari finished.");
            })
            .catch((err) => {
              reject(err);
            });
        });
      });
    });
  }
};
