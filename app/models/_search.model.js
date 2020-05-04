module.exports = (sequelize, Sequelize) => {
  const Search = sequelize.define(
    "search",
    {
      keyword: {
        type: Sequelize.STRING,
        allowNull: false,
      },
      platform: {
        type: Sequelize.STRING,
        allowNull: false,
      },
      hash: {
        type: Sequelize.TEXT,
        allowNull: false,
      },
    },
    {
      freezeTableName: false,
      timestamps: false,
      indexes: [
        {
          fields: ["hash"],
        },
      ],
    }
  );

  return Search;
};
