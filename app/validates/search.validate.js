/* eslint-disable node/no-unsupported-features */
import { check } from 'express-validator';
import { checkArray } from '../services/validate.service.js';
import {
  types,
  platforms,
  productStatuses,
  salesStatuses,
  deliveryCosts,
  sortOrders,
  searchRange,
} from './params/search.param.js';

const searchValidator = [
  check('type').isString().isIn(types).withMessage('Search type is invalid.'),
  check('page')
    .isInt({ leading_zeroes: false })
    // .isInt({ min: 1, max: 10, leading_zeroes: false })
    .withMessage('Page number is invalid.'),
  // check('category')
  //   .isObject()
  //   .custom((arr) => {
  //     return checkObject(arr);
  //   })
  //   .withMessage(
  //     'Category should be the object that has specific keys and values.',
  //   ),
  check('keyword').notEmpty().withMessage('Search keyword is required.'),
  check('negKeyword')
    .isString()
    .withMessage('Negative keyword needs to be string.'),
  check('platforms')
    .isArray({ min: 1, max: 7 })
    .custom((arr) => {
      return checkArray(platforms, arr);
    })
    .withMessage('Platforms are required.'),
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

export default searchValidator;
