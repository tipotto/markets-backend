const db = require("../models");
const UserService = require("../services/user.service");

/**
 * ユーザー作成
 */
exports.create = (req, res) => {
  // Validate request
  // if (!req.body.title) {
  //   res.status(400).send({
  //     message: "Content can not be empty!"
  //   });
  //   return;
  // }

  const user = {
    name: req.body.name,
    email: req.body.email,
    password: req.body.password
  };

  UserService.init(res).createUser(user);
};

/**
 * ユーザー一覧の取得
 */
exports.findAll = (req, res) => {
  // const name = req.query.name;
  // var condition = name ? { name: { [Op.like]: `%${name}%` } } : null;

  UserService.init(res).findAll();
};

/**
 * 特定のユーザーを取得
 */
exports.findOne = (req, res) => {
  const id = req.params.id;
  UserService.init(res).findOne(id);
};

/**
 * ユーザー情報の更新
 */
exports.update = (req, res) => {
  const id = req.params.id;
  UserService.init(res).update(id, req);
};

/**
 * 特定のユーザーの削除
 */
exports.delete = (req, res) => {
  const id = req.params.id;
  UserService.init(res).delete(id);
};

/**
 * 全てのユーザーを削除
 */
exports.deleteAll = (req, res) => {
  UserService.init(res).deleteAll();
};
