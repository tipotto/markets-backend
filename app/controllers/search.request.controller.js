/* eslint-disable node/no-unsupported-features */
const searchRequestController = (req, res, next) => {
  let { body } = req;
  const { minPrice, maxPrice, productStatus } = body;
  // const { category, minPrice, maxPrice, productStatus } = body;
  // body.category = Array.isArray(category) ? category[0] : {};
  body.minPrice = minPrice ? Number(minPrice) : 0;
  body.maxPrice = maxPrice ? Number(maxPrice) : 0;
  body.productStatus = productStatus.length > 0 ? productStatus : ['all'];
  next();
};

export default searchRequestController;
