const db = require("../models");
const ItemService = require("../services/item.service");

/**
 * アイテム作成
 */
exports.create = (req, res) => {
  // Validate request
  // if (!req.body.title) {
  //   res.status(400).send({
  //     message: "Content can not be empty!"
  //   });
  //   return;
  // }

  const item = {
    title: req.body.title,
    description: req.body.description,
    userId: req.body.userId
  };

  ItemService.init(res).create(item);
};

/**
 * アイテム一覧の取得
 */
exports.findAll = (req, res) => {
  // const name = req.query.name;
  // var condition = name ? { name: { [Op.like]: `%${name}%` } } : null;

  ItemService.init(res).findAll();
};

/**
 * 特定のアイテムを取得
 */
exports.findOne = (req, res) => {
  const id = req.params.id;
  ItemService.init(res).findOne(id);
};

/**
 * アイテム情報の更新
 */
exports.update = (req, res) => {
  const id = req.params.id;
  ItemService.init(res).update(id, req);
};

/**
 * 特定のアイテムの削除
 */
exports.delete = (req, res) => {
  const id = req.params.id;
  ItemService.init(res).delete(id);
};

/**
 * 全てのアイテムを削除
 */
exports.deleteAll = (req, res) => {
  ItemService.init(res).deleteAll();
};
