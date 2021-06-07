module.exports = (req, res, next) => {
  let { body } = req;
  const {
    category,
    minPrice,
    maxPrice,
    productStatus,
    salesStatus,
    deliveryCost,
    sortOrder,
    keywordFilter,
  } = body;
  body.category = Array.isArray(category) ? category[0] : {};
  body.minPrice = minPrice ? minPrice : 0;
  body.maxPrice = maxPrice ? maxPrice : 0;
  body.productStatus = productStatus.length > 0 ? productStatus : ['all'];
  body.salesStatus = salesStatus ? salesStatus : 'selling';
  body.deliveryCost = deliveryCost ? deliveryCost : 'all';
  body.sortOrder = sortOrder ? sortOrder : 'asc';
  body.sortOrder = sortOrder ? sortOrder : 'asc';
  body.keywordFilter = keywordFilter ? keywordFilter : 'use';
  next();
};
