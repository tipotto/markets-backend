module.exports = {
  HOST: "localhost",
  USER: "tipotto",
  PASSWORD: "L1keana5234",
  DB: "my_app",
  dialect: "mysql",
  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000
  }
};
