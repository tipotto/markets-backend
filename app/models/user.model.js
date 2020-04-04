module.exports = (sequelize, Sequelize) => {
  const User = sequelize.define(
    "user",
    {
      // id, createdAt, updatedAt はデフォルトで設定される。
      // id: not null, primary key, auto_increment
      // name, email, password: デフォルトでは varchar(255) が設定され、
      // not nullではないので注意。
      userId: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        autoIncrement: true,
        allowNull: false
      },
      name: {
        type: Sequelize.STRING,
        allowNull: false
      },
      email: {
        type: Sequelize.STRING,
        unique: true,
        allowNull: false
      },
      password: {
        type: Sequelize.STRING,
        allowNull: false
      }
    },
    {
      freezeTableName: false,
      timestamps: true,
      indexes: [
        {
          fields: ["userId"]
        },
        {
          fields: ["email"]
        }
      ]
    }
  );

  return User;
};
