const { check } = require("express-validator");
const ValidateService = require("../services/validate.service");
const SearchParam = require("./search.param");

module.exports = [
  check("category")
    .isArray({ min: 1, max: 1 })
    .custom((arr) => {
      return ValidateService.checkObjElems(arr);
    })
    .withMessage("Category should be the array that has at least one object."),
  check("keyword").notEmpty().withMessage("Search keyword is required."),
  check("platforms")
    .isArray({ min: 1, max: 3 })
    .custom((arr) => {
      return ValidateService.checkArrElems(SearchParam.platforms, arr);
    })
    .withMessage("Platforms are required."),
  check("minPrice")
    .isString()
    .isInt({ min: 0, max: 99999999, leading_zeroes: false })
    .isCurrency({
      // symbol: '¥',  // 通貨シンボル
      require_symbol: false, // 通貨シンボル（$, ¥）が必要かどうか
      allow_negatives: false, // マイナスの数字はOKかどうか
      allow_decimal: false, // 小数点はOKかどうか
    })
    .withMessage("Min-price is invalid."),
  check("maxPrice")
    .isString()
    .isInt({ min: 0, max: 99999999, leading_zeroes: false })
    .isCurrency({
      // symbol: '¥',  // 通貨シンボル
      require_symbol: false, // 通貨シンボル（$, ¥）が必要かどうか
      allow_negatives: false, // マイナスの数字はOKかどうか
      allow_decimal: false, // 小数点はOKかどうか
    })
    .withMessage("Max-price is invalid."),
  check("productStatus")
    .isArray({ min: 0, max: 6 })
    .custom((arr) => {
      return ValidateService.checkArrElems(SearchParam.productStatuses, arr);
    })
    .withMessage("Product status is invalid."),
  check("salesStatus")
    .isString()
    .isIn(SearchParam.salesStatuses)
    .withMessage("Sales status is invalid."),
  check("deliveryCost")
    .isString()
    .isIn(SearchParam.deliveryCosts)
    .withMessage("Delivery cost is invalid."),
  check("sortOrder")
    .isString()
    .isIn(SearchParam.sortOrders)
    .withMessage("Sort order is invalid."),
];
