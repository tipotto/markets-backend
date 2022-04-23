/* eslint-disable node/no-unsupported-features */
import { check } from 'express-validator';
import { checkArray } from '../services/validate.service.js';
import {
  platforms,
  searchRange,
  productStatuses,
  salesStatuses,
  deliveryCosts,
  sortOrders,
} from './params/analyze.param.js';

const analyzeValidator = [
  check('keyword').notEmpty().withMessage('Search keyword is required.'),
  check('negKeyword')
    .isString()
    .withMessage('Negative keyword needs to be string.'),
  check('platform')
    .isString()
    .isIn(platforms)
    .withMessage('Platform is invalid.'),
  // check('searchTarget')
  //   .isString()
  //   .isIn(searchTarget)
  //   .withMessage('Search target is invalid.'),
  // check('priceType')
  //   .isString()
  //   .isIn(priceType)
  //   .withMessage('Price type is invalid.'),
  check('searchRange')
    .isString()
    .isIn(searchRange)
    .withMessage('Search range is invalid.'),
  check('minPrice')
    .isInt({ min: 0, max: 99999999, leading_zeroes: false })
    .isCurrency({
      // symbol: '¥',  // 通貨シンボル
      require_symbol: false, // 通貨シンボル（$, ¥）が必要かどうか
      allow_negatives: false, // マイナスの数字はOKかどうか
      allow_decimal: false, // 小数点はOKかどうか
    })
    .withMessage('Min-price is invalid.'),
  check('maxPrice')
    .isInt({ min: 0, max: 99999999, leading_zeroes: false })
    .isCurrency({
      // symbol: '¥',
      require_symbol: false,
      allow_negatives: false,
      allow_decimal: false,
    })
    .withMessage('Max-price is invalid.'),
  check('productStatus')
    .isArray({ min: 1, max: 6 })
    .custom((arr) => {
      return checkArray(productStatuses, arr);
    })
    .withMessage('Product status is invalid.'),
  check('salesStatus')
    .isString()
    .isIn(salesStatuses)
    .withMessage('Sales status is invalid.'),
  check('deliveryCost')
    .isString()
    .isIn(deliveryCosts)
    .withMessage('Delivery cost is invalid.'),
  check('sortOrder')
    .isString()
    .isIn(sortOrders)
    .withMessage('Sort order is invalid.'),
];

export default analyzeValidator;
