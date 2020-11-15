const SearchService = require('../services/search.service');
// const logger = require("../config/log4js.config.js");

module.exports = (req, res) => {
  const form = {
    keyword: req.body.keyword,
    pfArray: req.body.platform,
    resultNum: Number(req.body.resultNum),
    sortIndex: req.body.sortIndex,
    sortOrder: req.body.sortOrder,
  };

  SearchService.init(res)
    .search(form)
    .then((items) => {
      console.log('controller: ' + items);
      console.log('正常に処理が完了しました。');
    })
    .catch((err) => {
      console.log('エラーが発生しました: ' + err.message);
    });
};
