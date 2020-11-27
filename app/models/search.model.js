module.exports = (sequelize, Sequelize) => {
  const Search = sequelize.define(
    'search',
    {
      results: {
        type: Sequelize.TEXT,
        get() {
          return JSON.parse(this.getDataValue('results'));
        },
        set(val) {
          return this.setDataValue('results', JSON.stringify(val));
        },
      },
      cacheKey: {
        type: Sequelize.STRING,
        allowNull: false,
      },
    },
    {
      freezeTableName: false,
      timestamps: false,
      indexes: [
        {
          fields: ['cacheKey'],
        },
      ],
    }
  );

  return Search;
};
