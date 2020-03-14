module.exports = (sequelize, Sequelize) => {
  const Item = sequelize.define("item", {
    title: {
      type: Sequelize.STRING
    },
    description: {
      type: Sequelize.STRING
    }
    // password: {
    //   type: Sequelize.STRING
    // }
  });

  return Item;
};
