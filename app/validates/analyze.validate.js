const { check } = require('express-validator');
const validate = require('../services/validate.service');
const {
  platforms,
  searchTarget,
  priceType,
  searchRange,
  productStatuses,
  deliveryCosts,
  sortOrders,
} = require('./params/analyze.param');

module.exports = [
  check('keyword').notEmpty().withMessage('Search keyword is required.'),
  check('negKeyword')
    .isString()
    .withMessage('Negative keyword needs to be string.'),
  check('platform')
    .isString()
    .isIn(platforms)
    .withMessage('Platform is invalid.'),
  check('searchTarget')
    .isString()
    .isIn(searchTarget)
    .withMessage('Search target is invalid.'),
  check('priceType')
    .isString()
    .isIn(priceType)
    .withMessage('Price type is invalid.'),
  check('searchRange')
    .isString()
    .isIn(searchRange)
    .withMessage('Search range is invalid.'),
  check('productStatus')
    .isArray({ min: 1, max: 6 })
    .custom((arr) => {
      return validate.checkArray(productStatuses, arr);
    })
    .withMessage('Product status is invalid.'),
  check('deliveryCost')
    .isString()
    .isIn(deliveryCosts)
    .withMessage('Delivery cost is invalid.'),
  check('sortOrder')
    .isString()
    .isIn(sortOrders)
    .withMessage('Sort order is invalid.'),
];
