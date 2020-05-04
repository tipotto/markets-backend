const crypto = require("crypto");
const db = require("../models/index");
const Search = db.search;
const Op = db.Sequelize.Op;
const Key = require("../constants/search");
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
   * アイテムリストを全て削除（クーロン処理）
   */
  static deleteAll() {
    return new Promise((resolve, reject) => {
      Search.destroy({
        where: {},
        truncate: false,
      })
        .then(resolve)
        .catch(reject);
    });
  }

  /**
   * 配列の登録
   * @param {*} resultArray
   */
  bulkCreate(resultArr) {
    console.log("3. 検索結果をDBに登録。");

    var promise = resultArr.map((arr) => {
      return new Promise((resolve, reject) => {
        Search.bulkCreate(arr).then(resolve).catch(reject);
      });
    });
    return Promise.all(promise);
  }

  findOne(hash) {
    console.log("4. findOneメソッド実行。");
    return new Promise((resolve, reject) => {
      Search.findOne({
        where: {
          hash: hash,
        },
      })
        .then(resolve)
        .catch(reject);
    });
  }

  /**
   * アイテムリストの取得
   * @param {*} form
   */
  findAll(form) {
    console.log("4. スクレイピング結果の取得。");
    return new Promise((resolve, reject) => {
      Search.findAll({
        where: {
          hash: {
            [Op.or]: form.hashArr,
          },
        },
        limit: form.resultNum,
        order: [[form.sortIndex, form.sortOrder]],
      })
        .then(resolve)
        .catch(reject);
    });
  }

  response(value) {
    this.res.status(200).send(value);
  }

  /**
   * スクレイピング
   * @param {*} form
   */
  scrape(form) {
    return new Promise((resolve, reject) => {
      console.log("1. python-shellの呼び出し。");
      var pyshell = new PythonShell(Key.PYTHON_PATH, {
        mode: "text",
      });

      var json = {
        paramArr: form.paramArr,
        keyword: form.keyword,
      };

      console.log("2. フォームデータをpython側に送信。");
      pyshell.send(JSON.stringify(json));

      pyshell.on("message", (data) => {
        console.log("検索結果： " + data);

        const resultArr = JSON.parse(data || "null");
        this.bulkCreate(resultArr)
          .then(this.findAll.bind(null, form))
          .then(this.response.bind(this))
          .catch(reject);
      });

      pyshell.end((err) => {
        if (err) reject(err);
        console.log("7. 一通り処理を終了。");
        resolve("スクレイピング完了。");
      });
    });
  }

  generateHash(keyword, platform) {
    console.log("3. ハッシュを生成。");
    const sha1sum = crypto.createHash("sha1");
    sha1sum.update(keyword + platform + Key.HASH_SECRET);
    return sha1sum.digest("hex");
  }

  moldKeyword(keyword) {
    console.log("1. 検索キーワードを成形。");
    return keyword.split(/\s+/).join("_");
  }

  addFormProps(form, value) {
    console.log("6. addFormPropsメソッド実行。");

    return new Promise((resolve, reject) => {
      var hashArr = [];
      var scrapeParamArr = [];
      value.forEach((obj) => {
        hashArr.push(obj.hash);
        if (obj.platform) {
          scrapeParamArr.push({
            hash: obj.hash,
            platform: obj.platform,
          });
        }
      });
      form.hashArr = hashArr;
      form.paramArr = scrapeParamArr;
      resolve(form);
    });
  }

  createObj(hash, platform, value) {
    console.log("5. createArrメソッド実行。");

    return new Promise((resolve, reject) => {
      var obj = {};
      obj.hash = hash;
      if (!value) obj.platform = platform;
      resolve(obj);
    });
  }

  checkCache(form, keyword) {
    console.log("2. checkCacheメソッド実行。");

    const arr = form.pfArray;
    var promise = arr.map((platform) => {
      return new Promise((resolve, reject) => {
        const hash = this.generateHash(keyword, platform);
        this.findOne(hash)
          .then(this.createObj.bind(null, hash, platform))
          .then(resolve)
          .catch(reject);
      });
    });
    return Promise.all(promise);
  }

  search(form) {
    return new Promise((resolve, reject) => {
      const moldedKeyword = this.moldKeyword(form.keyword);
      this.checkCache(form, moldedKeyword)
        .then(this.addFormProps.bind(null, form))
        .then(this.scrape.bind(this))
        .then(resolve)
        .catch(reject);
    });
  }
};
