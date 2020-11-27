const SearchService = require('../services/search.service');
// const logger = require("../config/log4js.config.js");

module.exports = (req, res) => {
  const form = {
    query: req.body.keyword,
    platforms: req.body.platform,
    resultNum: Number(req.body.resultNum),
    sortIndex: req.body.sortIndex,
    sortOrder: req.body.sortOrder,
  };

  SearchService.init()
    .search(form)
    .then((results) => {
      res.status(200).send(results);
      console.log('正常に処理が完了しました。');
    })
    .catch((err) => {
      // TODO クライアントにエラーを返すように実装
      console.log('エラーが発生しました: ' + err.message);
    });
};
