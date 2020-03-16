module.exports = (sequelize, Sequelize) => {
  const User = sequelize.define("user", {
    // id, createdAt, updatedAt はデフォルトで設定される。
    // id: not null, primary key, auto_increment
    // name, email, password: デフォルトでは varchar(255) が設定され、
    // not nullではないので注意。
    name: {
      type: Sequelize.STRING
    },
    email: {
      type: Sequelize.STRING
    },
    password: {
      type: Sequelize.STRING
    }
  });

  return User;
};
