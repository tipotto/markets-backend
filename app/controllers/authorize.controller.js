const httpLogger = require("../config/log4js.config.js").http;
const RequestError = require("../exceptions/RequestError");

module.exports = (req, res, next) => {
  const checkCustomHeaders = () => {
    console.log("Custom header check...");
    if (
      !(
        req.header("Content-Type") &&
        req.header("Content-Type") === "application/json"
      ) ||
      !(
        req.header("X-Requested-With") &&
        req.header("X-Requested-With") === "fetch"
      ) ||
      !(
        req.header("X-Requested-By") &&
        req.header("X-Requested-By") === "markets.jp"
      )
    ) {
      console.log("Custom header check error...");
      throw new RequestError("Server has gotten an invalid request.");
    }
    console.log("Custom headers exist...");
  };

  const responseHeaders = () => {
    // 許可されるオリジン
    res.header("Access-Control-Allow-Origin", "http://localhost:8080");

    // 許可されるメソッド
    res.header("Access-Control-Allow-Methods", "POST,OPTIONS");

    // 許可されるヘッダ
    res.header(
      "Access-Control-Allow-Headers",
      "Origin,Referer,Content-Type,X-Requested-With,X-Requested-By"
      // "Origin, X-Requested-With, Content-Type, Accept"
    );

    // プリフライト情報のキャッシュを保持できる時間
    // この期間内であれば、同一URLに対するリクエストの際にキャッシュが適用される
    // 10日間はキャッシュを利用
    res.header("Access-Control-Max-Age", "864000");
  };

  const checkRequest = () => {
    const origin = "http://localhost:8080";
    const referrer = "http://localhost:8000/";
    if (
      !(req.header("Origin") && req.header("Origin") === origin) ||
      !(req.header("Referer") && req.header("Referer") === referrer) ||
      !(
        req.header("Access-Control-Request-Method") &&
        req.header("Access-Control-Request-Method") === "POST"
      ) ||
      !(
        req.header("Access-Control-Request-Headers") &&
        req.header("Access-Control-Request-Headers") ===
          "Content-Type,X-Requested-With,X-Requested-By"
      )
    ) {
      throw new RequestError("Server has gotten an invalid request.");
    }
  };

  // エラーを仲介して呼び出し元にスローする場合には、try-catchは必要ない？
  const checkPreflight = () => {
    // リクエストのチェック
    checkRequest();

    // プリフライトリクエストのレスポンス
    responseHeaders();
  };

  try {
    console.log("method", req.method);
    if (req.method === "POST") {
      checkCustomHeaders();
      httpLogger.info("Custom headers in the request is valid.");
      next();
    } else {
      checkPreflight();
      res.status(200).json({ result: "OK" });
      httpLogger.info("Preflight request is valid.");
    }
  } catch (e) {
    res.status(403).json({ error: "Forbidden" });
    httpLogger.error(e);
  }
};
