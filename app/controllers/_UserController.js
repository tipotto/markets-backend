// Models を読み込む
const Models = require("../models/_models");

class UsersController {
  /** 検索するアクション */
  findAll(req, res) {
    // オプションの雛形を作っておく
    const options = {
      where: {}
    };

    // リクエストで address パラメータを指定されていれば、絞り込み検索のためのオプションとして追加する
    if (req.query["address"]) {
      options.where["address"] = req.query["address"];
    }

    // User モデルを使用する
    Models.User.findAll(options)
      .then(result => {
        // 200:OK と、JSON 形式の結果データ dataValues を返す
        res.status(200);
        res.json(result.dataValues);
      })
      .catch(error => {
        // 404:NotFound と、エラー情報を返す
        res.status(404);
        res.json(error);
      });
  }
}
