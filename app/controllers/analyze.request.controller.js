/* eslint-disable node/no-unsupported-features */
const analyzeRequestController = (req, res, next) => {
  let { body } = req;
  const { minPrice, maxPrice, productStatus } = body;
  body.minPrice = minPrice ? Number(minPrice) : 0;
  body.maxPrice = maxPrice ? Number(maxPrice) : 0;
  body.productStatus = productStatus.length > 0 ? productStatus : ['all'];
  next();
};

export default analyzeRequestController;
