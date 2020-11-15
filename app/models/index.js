const config = require('../config/db.config.js');
const Sequelize = require('sequelize');

const sequelize = new Sequelize(config.DB, config.USER, config.PASSWORD, {
  host: config.HOST,
  dialect: config.DIALECT,
  pool: config.CONNECTION_POOL,
  operatorsAliases: false,
});

const db = {};

db.Sequelize = Sequelize;
db.sequelize = sequelize;

db.search = require('./search.model.js')(sequelize, Sequelize);
module.exports = db;
