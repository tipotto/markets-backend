// 型定義用に require しておく
const Sequelize = require("sequelize");

module.exports = sequelize => {
  const UserModel = sequelize.define("users", {
    // CREATE TABLE 文で指定した内容は大体以下のような感じ
    // INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT
    id: {
      field: "id",
      type: Sequelize.INTEGER(11),
      primaryKey: true,
      autoIncrement: true
    },
    // VARCHAR(100) NOT NULL
    userName: {
      field: "user_name",
      type: Sequelize.STRING(100),
      allowNull: false
    },
    // VARCHAR(500) DEFAULT NULL
    address: { field: "address", type: Sequelize.STRING(500) },
    // DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    createdAt: { field: "created_at", type: Sequelize.DATE },
    // DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    updatedAt: { field: "updated_at", type: Sequelize.DATE }
  });
  return UserModel;
};
