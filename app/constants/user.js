/**
 * 成功時のメッセージ/ステータスコード
 */
const create_success = {
  message: "User was created successfully.",
  httpResCode: 201
};

const fetch_success = {
  message: "User was fetched successfully.",
  httpResCode: 200
};

const delete_success = {
  message: "User was deleted successfully.",
  httpResCode: 204
};

const update_success = {
  message: "User was updated successfully.",
  httpResCode: 204
};

/**
 * 失敗時のメッセージ/ステータスコード
 */
const create_fail = {
  message: "Error occurred while creating the user.",
  httpResCode: 409
};

const fetch_fail = {
  message: "Error occurred while fetching the user.",
  httpResCode: 404
};

const delete_fail = {
  message: "Error occurred while deleting the user.",
  httpResCode: 409
};

const update_fail = {
  message: "Error occurred while updating the user.",
  httpResCode: 409
};

/**
 * 作成
 */
const create = {
  SUCCESS: create_success,
  FAIL: create_fail
};

/**
 * 取得
 */
const fetch = {
  SUCCESS: fetch_success,
  FAIL: fetch_fail
};

/**
 * 削除
 */
const remove = {
  SUCCESS: delete_success,
  FAIL: delete_fail
};

/**
 * 更新
 */
const update = {
  SUCCESS: update_success,
  FAIL: update_fail
};

module.exports = {
  CREATE: create,
  FETCH: fetch,
  DELETE: remove,
  UPDATE: update
};

// exports.success = success;
// exports.error = error;
// exports.res = res;
