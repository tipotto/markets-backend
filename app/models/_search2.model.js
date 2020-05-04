module.exports = (sequelize, Sequelize) => {
  const Item = sequelize.define(
    "item",
    {
      title: {
        type: Sequelize.STRING,
        allowNull: false
      },
      description: {
        type: Sequelize.TEXT,
        allowNull: false
      },
      userId: {
        type: Sequelize.INTEGER,
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
          fields: ["createdAt"]
        }
      ]
    }
  );

  return Item;
};
