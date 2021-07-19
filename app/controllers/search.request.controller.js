module.exports = (req, res, next) => {
  let { body } = req;
  const { category, minPrice, maxPrice, productStatus } = body;
  body.category = Array.isArray(category) ? category[0] : {};
  body.minPrice = minPrice ? minPrice : 0;
  body.maxPrice = maxPrice ? maxPrice : 0;
  body.productStatus = productStatus.length > 0 ? productStatus : ['all'];
  next();
};
