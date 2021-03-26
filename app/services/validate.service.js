const SearchParam = require("../validates/search.param");

module.exports = class ValidateService {
  static checkObjElems(arr) {
    const obj = arr[0];
    if (typeof obj !== "object") return false;
    if (Object.keys(obj).length !== 2) return false;

    const objArr = Object.keys(obj).map((key) => {
      if (!SearchParam.categoryObjKeys.includes(key)) return false;

      const value = obj[key];
      if (key === "main") {
        if (SearchParam.mainCategories.includes(value)) return true;
      } else {
        if (SearchParam.subCategories.includes(value)) return true;
      }
      return false;
    });

    return objArr.includes(false) ? false : true;
  }

  static checkArrElems(arr, targetArr) {
    if (!targetArr.length) return true;
    const elemArr = targetArr.map((value) => {
      return arr.includes(value);
    });
    return elemArr.includes(false) ? false : true;
  }

  //   static checkCurrency(value) {
  //     if (!value) return "0";
  //     return value;
  //   }
};
