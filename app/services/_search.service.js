const db = require("../models/index");
const Search = db.search;
// const res = require("../constants/user");

const key = require("../constants/search");
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
   * 成功時の処理
   * @param {*} resData
   * @param {*} resolve
   */
  success(resData, resolve) {
    // this.res.status(resData.httpResCode).send({
    //   message: resData.message
    // });
    // TODO 上の処理の後に、以下の処理が実行されるか確認。
    // TODO 以下のclose処理の有無でどのような違いがあるのかを調べる。
    // db.sequelize.close();
    resolve();
  }

  /**
   * エラー発生時の処理
   * @param {*} resData
   * @param {*} reject
   */
  error(resData, reject) {
    // TODO エラーオブジェクトを受け取ってエラーメッセージを返すべきか検討。
    // 抽象的なメッセージでは、エラーの箇所や原因を特定しづらいため、
    // エラーオブジェクトを受け取る方が良さそう。
    this.res.status(resData.httpResCode).send({
      message: resData.message
      // message: err ? err.message : resData.message
    });
    db.sequelize.close();
    // TODO rejectが呼ばれた際、promiseオブジェクトはthenで受け取るのか、
    // それともcatchで受け取るのか調べる。（おそらくcatch？）
    // resolve, rejectのいずれが呼ばれた場合でも、promiseオブジェクトが返されるという認識。
    // しかし、どちらが呼ばれるかによって、結果の受け取り場所が異なるのか？（then or catch）
    reject(err);
  }

  /**
   * フロントエンドへのレスポンス処理
   * @param {*} items
   * @param {*} resData
   * @param {*} resolve
   */
  resData(items, resData, resolve) {
    // TODO sendメソッドを使うと、フロントエンドにデータを返せるのか調べる。
    // また、他にどのような実装が必要なのかも調べる。
    this.res.status(resData.httpResCode).send(items);
    db.sequelize.close();
    resolve("findAllメソッドを実行完了。");
    // resolve({ items: data });
  }

  /**
   *
   * update, delete メソッドで使用する。
   * どちらも成功時は204, 失敗時は409を返すため、
   * メソッドの引数ではなく、内部的にステータスコードを渡している。
   * @param {*} num
   * @param {*} id
   */
  // resByNum(num, id, resAction) {
  //   if (num == 1) this.success(resAction.SUCCESS);
  //   else this.error(null, id, resAction.FAIL);
  // }

  //   errorWithId(err, id) {
  //     this.res.status(500).send({
  //       message: err ? err.message : "Sorry, error occurred with id =" + id
  //     });
  //   }

  /**
   * メルカリ検索
   * @param {*} keyword
   */
  static mercari(keyword) {
    return new Promise((resolve, reject) => {
      var pyshell = new PythonShell(key.pyPath.MERCARI);
      pyshell.send(keyword);

      // pythonでprintメソッドによって出力されたテキストは、dataに格納される。
      // 例外発生時のexcept内のテキストを含む。
      pyshell.on("message", data => {
        console.log("mercari：" + data);
      });

      // このセクションでエラーを受け取ることは、今のところなさそう。
      // pythonのexcept句で処理できないエラーが発生したとしても、
      // この部分では受け取れないため、スルーされる。
      // スクレイピング処理、dataframeへのデータの格納時にエラーが発生した場合、
      // expect句で処理されるように実装済み。
      pyshell.end(err => {
        // if (err) reject("異常系：" + err);
        console.log("end");
        resolve("mercari finished.");
      });
    });
  }

  /**
   * ラクマ検索
   * @param {*} keyword
   */
  static rakuten(keyword) {
    return new Promise((resolve, reject) => {
      var pyshell = new PythonShell(key.pyPath.RAKUTEN);
      pyshell.send(keyword);

      pyshell.on("message", data => {
        console.log("Rakuten：" + data);
      });

      pyshell.end(err => {
        console.log("end");
        resolve("Rakuten finished.");
      });
    });
  }

  /**
   * アイテムリストの取得
   * @param {*} resultNum
   * @param {*} sortIndex
   * @param {*} sortOrder
   */
  // resultNum: number (検索結果の取得上限数)
  // sortIndex: string (title, price, platform etc.)
  // sortOrder: string (ASC/DESC)
  findAll(resultNum, sortIndex, sortOrder) {
    return new Promise((resolve, reject) => {
      Search.findAll({
        limit: resultNum,
        order: [[sortIndex, sortOrder]]
        // where: {}
      })
        .then(items => {
          // this.res.status(res.FETCH.SUCCESS.httpResCode).send(items);
          resolve(items);
        })
        .catch(err => {
          // this.res.status(res.FETCH.FAIL.httpResCode).send({
          //   message: err.message
          // });
          // TODO rejectが呼ばれた際、promiseオブジェクトはthenで受け取るのか、
          // それともcatchで受け取るのか調べる。（おそらくcatch？）
          // resolve, rejectのいずれが呼ばれた場合でも、promiseオブジェクトが返されるという認識。
          // しかし、どちらが呼ばれるかによって、結果の受け取り場所が異なるのか？（then or catch）
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
        truncate: false
      })
        .then(() => {
          resolve();
        })
        .catch(err => {
          reject(err);
        });
    });
  }
};
