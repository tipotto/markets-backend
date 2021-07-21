const {
  categoryObjKeys,
  mainCategories,
  subCategories,
} = require('../validates/params/search.param');

module.exports = class ValidateService {
  static checkObject(obj) {
    if (typeof obj !== 'object') return false;
    if (Object.keys(obj).length !== 2) return false;

    const objArr = Object.keys(obj).map((key) => {
      if (!categoryObjKeys.includes(key)) return false;

      const value = obj[key];
      if (!value) return true;

      if (key === 'main') {
        if (mainCategories.includes(value)) return true;
      } else {
        if (subCategories.includes(value)) return true;
      }
      return false;
    });

    return objArr.includes(false) ? false : true;
  }

  static checkArray(arr, targetArr) {
    if (!targetArr.length) return false;
    const elemArr = targetArr.map((value) => {
      return arr.includes(value);
    });
    return elemArr.includes(false) ? false : true;
  }
};
