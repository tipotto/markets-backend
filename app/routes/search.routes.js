module.exports = app => {
  const search = require("../controllers/search.controller.js");

  var router = require("express").Router();

  router.post("/", search.search);

  // router.post("/mercari", search.mercari);
  // router.post("/rakuten", search.rakuten);
  // router.post("/yahoo", search.yahoo);

  app.use("/api/search", router);
};
