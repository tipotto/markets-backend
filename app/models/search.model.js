module.exports = (sequelize, Sequelize) => {
  const Search = sequelize.define(
    "items",
    {
      // id, createdAt, updatedAt はデフォルトで設定される。
      // id: not null, primary key, auto_increment
      // name, email, password: デフォルトでは varchar(255) が設定され、
      // not nullではないので注意。

      // id: {
      //   type: Sequelize.INTEGER,
      //   primaryKey: true,
      //   autoIncrement: true,
      //   allowNull: false
      // },
      title: {
        type: Sequelize.STRING,
        allowNull: false,
      },
      price: {
        type: Sequelize.INTEGER,
        allowNull: false,
      },
      imageUrl: {
        type: Sequelize.TEXT,
        allowNull: false,
      },
      detailUrl: {
        type: Sequelize.TEXT,
        allowNull: false,
      },
      platform: {
        type: Sequelize.STRING,
        allowNull: false,
      },
      hash: {
        type: Sequelize.STRING,
        allowNull: false,
      },
    },
    {
      freezeTableName: false,
      timestamps: false,
      indexes: [
        {
          fields: ["price"],
        },
        {
          fields: ["hash"],
        },
      ],
    }
  );

  return Search;
};
