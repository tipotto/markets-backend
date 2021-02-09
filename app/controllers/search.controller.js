const SearchService = require('../services/search.service');
// const logger = require("../config/log4js.config.js");

module.exports = (req, res) => {
  const form = {
    category: req.body.category[0],
    query: req.body.keyword,
    platforms: req.body.platforms,
    minPrice: req.body.minPrice,
    maxPrice: req.body.maxPrice,
    productStatus: req.body.productStatus,
    salesStatus: req.body.salesStatus ? req.body.salesStatus : 'selling',
    deliveryCost: req.body.deliveryCost,
    sortOrder: req.body.sortOrder ? req.body.sortOrder : 'asc',
  };

  SearchService.init()
    .search(form)
    .then((results) => {
      console.log('results', results);
      res.status(200).send(results);
      console.log('正常に処理が完了しました。');
    })
    .catch((err) => {
      // TODO クライアントにエラーを返すように実装
      console.log('エラーが発生しました: ' + err.message);
    });
};
