const SearchService = require("../services/search.service");
const db = require("../models/index");
const Key = require("../constants/user");
// const logger = require("../config/log4js.config.js");

exports.search = (req, res) => {
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
      console.log("controller: " + items);
      console.log("正常に処理が完了しました。");
    })
    .catch((err) => {
      console.log("エラーが発生しました: " + err.message);
    });
};
