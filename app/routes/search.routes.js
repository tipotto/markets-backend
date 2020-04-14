module.exports = (app) => {
  const search = require("../controllers/search.controller.js");

  var router = require("express").Router();
  router.post("/", search.search);
  app.use("/api/search", router);
};
