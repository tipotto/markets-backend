const db = require("../models/index");
const User = db.user;
const res = require("../constants/user");
// const Op = db.Sequelize.Op;
// const res = consts.res;

module.exports = class UserService {
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
    return new UserService(res);
  }

  success(resData) {
    this.res.status(resData.httpResCode).send({
      message: resData.message
    });
  }

  /**
   * エラー
   * @param {*} err
   * @param {*} id
   * @param {*} httpResCode
   */
  error(err, id, resData) {
    let errorText;
    if (id) errorText = resData.message + "with id =" + id;
    else errorText = resData.message;

    this.res.status(resData.httpResCode).send({
      message: err ? err.message : errorText
    });
  }

  /**
   * レスポンス（データを返す場合）
   * @param {*} data
   * @param {*} httpResCode
   */
  resData(data, resData) {
    this.res.status(resData.httpResCode).send(data);
  }

  /**
   *
   * update, delete メソッドで使用する。
   * どちらも成功時は204, 失敗時は409を返すため、
   * メソッドの引数ではなく、内部的にステータスコードを渡している。
   * @param {*} num
   * @param {*} id
   */
  resByNum(num, id, resAction) {
    if (num == 1) this.success(resAction.SUCCESS);
    else this.error(null, id, resAction.FAIL);
  }

  //   errorWithId(err, id) {
  //     this.res.status(500).send({
  //       message: err ? err.message : "Sorry, error occurred with id =" + id
  //     });
  //   }

  /**
   * ユーザー作成
   * @param {*} user
   */
  createUser(user) {
    User.create(user)
      .then(data => this.resData(data, res.CREATE.SUCCESS))
      .catch(err => this.error(err, null, res.CREATE.FAIL));
  }

  /**
   * ユーザー一覧の取得
   */
  findAll() {
    User.findAll({ where: {} })
      .then(data => this.resData(data, res.FETCH.SUCCESS))
      .catch(err => this.error(err, null, res.FETCH.FAIL));
  }

  /**
   * 特定のユーザーを取得
   * @param {*} id
   */
  findOne(id) {
    User.findByPk(id)
      .then(data => this.resData(data, res.FETCH.SUCCESS))
      .catch(err => this.error(err, id, res.FETCH.FAIL));
  }

  /**
   * ユーザー情報の更新
   * @param {*} id
   * @param {*} req
   */
  update(id, req) {
    User.update(req.body, {
      where: { id: id }
    })
      .then(num => this.resByNum(num, id, res.UPDATE))
      .catch(err => this.error(err, id, res.UPDATE.FAIL));
  }

  /**
   * 特定のユーザーの削除
   * @param {*} id
   */
  delete(id) {
    User.destroy({
      where: { id: id }
    })
      .then(num => this.resByNum(num, id, res.DELETE))
      .catch(err => this.error(err, id, res.DELETE.FAIL));
  }

  /**
   * 全てのユーザーを削除
   * thenメソッド内でnumsを受け取ることで、
   * 削除ユーザー数を取得できる。
   */
  deleteAll() {
    User.destroy({
      where: {},
      truncate: false
    })
      .then(() => this.success(res.DELETE.SUCCESS))
      .catch(err => this.error(err, res.DELETE.FAIL));
  }
};
