module.exports = (req, res, next) => {
  let { body } = req;
  const { productStatus } = body;
  body.productStatus = productStatus.length > 0 ? productStatus : ['all'];
  next();
};
