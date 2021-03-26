const SearchService = require("../services/search.service");
const httpLogger = require("../config/log4js.config.js").http;
const { validationResult } = require("express-validator");
const PyShellError = require("../exceptions/PyShellError");
const ParseError = require("../exceptions/ParseError");

module.exports = (req, res) => {
  // return res.status(422).json({ error: "The request data is invalid." });

  console.log("/api/search 2...");
  console.log("Search controller...");

  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    res.status(422).json({ error: "The request is invalid." });
    httpLogger.error(errors);
    return;
  }

  const form = {
    category: req.body.category[0],
    query: req.body.keyword,
    platforms: req.body.platforms,
    minPrice: req.body.minPrice,
    maxPrice: req.body.maxPrice,
    productStatus: req.body.productStatus.length
      ? req.body.productStatus
      : ["all"],
    salesStatus: req.body.salesStatus ? req.body.salesStatus : "selling",
    deliveryCost: req.body.deliveryCost ? req.body.deliveryCost : "all",
    sortOrder: req.body.sortOrder ? req.body.sortOrder : "asc",
  };

  console.log("form", form);

  SearchService.init()
    .search(form)
    .then(({ status, results, error }) => {
      res.status(200).json(results);

      if (status === "success") {
        httpLogger.info("All processes are successfully completed.");
      } else {
        httpLogger.error(error);
      }
    })
    .catch((e) => {
      if (e instanceof ParseError) {
        res.status(502).json({ error: "Bad Gateway" });
      } else if (e instanceof PyShellError) {
        res.status(500).json({ error: "Internal Server Error" });
      }
      httpLogger.error(e);
    });
};
