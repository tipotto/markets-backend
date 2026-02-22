# markets.jp (Backend)

<img width="800" alt="markets-top" src="https://github.com/user-attachments/assets/ed1dbf9f-b9e6-4649-968b-4d742146042d">
<img width="800" alt="markets-top" src="https://github.com/user-attachments/assets/8528d198-7233-4dc6-85be-b2dde8229278">
<img width="800" alt="markets-items" src="https://github.com/user-attachments/assets/3c000745-c76a-4be9-85c1-2586323551bc">

## サービス概要
「フリマサイト検索」と「フリマサイト分析」という２つの機能を提供しています。  
「フリマ 一括検索」などのキーワードで検索結果1位となり、累計800名以上の方にご利用いただきました（現在はクローズ済み）。

### 主な機能
#### フリマサイト検索
フリマサイト、ECサイトを一括検索し、価格順に表示するサービスです。

#### フリマサイト分析
現在の市場や過去の販売データをもとに、各サイトでの相場価格を算出するサービスです。

## 主な使用技術

言語：Node.js, Python  
フレームワーク：Express  
モジュール：asyncio, aiohttp etc.

フロントエンドは[こちら](https://github.com/tipotto/markets-client)

## 開発の背景
以前からフリマサービスやECサイトをよく利用しており、プラットフォームごとに商品のラインナップや検索オプションの充実度などが異なるため、1 つのプラットフォームから利用できるようにしたら便利ではないかと考え、開発しました。

初めての個人開発だったこともあり、フロントエンド、バックエンド共にそれまで触れたことのなかった技術を積極的に取り入れたことで、スキルの幅を大きく広げる良い経験になりました。

## サービスの特徴
### 対応プラットフォーム

- メルカリ
- ラクマ
- PayPay フリマ
- ヤフオク
- Amazon
- 楽天
- Yahooショッピング

### 検索オプション

- 商品カテゴリ（メインカテゴリ、サブカテゴリ）
- 価格
- 商品の状態
- 販売状況
- 配送料の有無
- 検索結果の並び順
