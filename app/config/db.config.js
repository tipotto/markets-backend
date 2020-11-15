module.exports = {
  HOST: 'localhost',
  USER: 'tipotto',
  PASSWORD: 'L1keana5234',
  DB: 'my_app',
  DIALECT: 'mysql',
  CONNECTION_POOL: {
    max: 5, // プールするコネクションの最大数
    min: 0, // プールするコネクションの最小数
    acquire: 30000, // プールがエラーをスローする前に、接続を試みる最大時間
    idle: 10000, // コネクションが確立する前にアイドル状態でいる最大時間
    // evict: 1000 // プールがアイドル状態のコネクションを削除する時間間隔
  },
};
