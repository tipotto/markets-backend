const Sequelize = require("sequelize");

// 接続情報 (省略)
// 接続開始 (省略)
const sequelize = new Sequelize(database, username, password, {
  host: host,
  dialect: "mysql",
  operatorsAliases: false
});

// モデルを定義する
const Models = {};

// 各モデルを設定する
Models.User = require("./_UserModel")(sequelize);
Models.Product = require("./product-model")(sequelize); // user-model.js 的なファイルがあるテイ

// Sequelize 本体を設定する
Models.sequelize = sequelize;
Models.Sequelize = Sequelize;

// エクスポートする
module.exports = Models;
