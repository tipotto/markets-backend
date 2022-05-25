#!/bin/bash
# restore-cache: Restore the npm cache from GCS.
# GCSのバケットからタイムスタンプを取得（存在しない場合は0）
# タイムスタンプが1ヶ月未満の場合、バケットからtgzファイルをコピーし、tmpフォルダ以下に配置
# ボリュームにキャッシュ保存用のディレクトリ（/home/cache/.npm）を作成
# 各ビルドステップをまたいで利用できるように、tgzファイルをそこに配置

set -e -u

TIMESTAMP=$(gsutil cat gs://$CACHE_BUCKET_NAME/timestamp || echo 0)
echo "timestamp fetched: $TIMESTAMP"

if (( $(date +%s) - $TIMESTAMP < $SECONDS_IN_A_MONTH )); then
  gsutil -q -m cp gs://$CACHE_BUCKET_NAME/npm.tgz /tmp 

  echo 'Restoring npm cache'
  mkdir $CACHE_DIR_PATH
  tar -xzf /tmp/npm.tgz -C $CACHE_DIR_PATH
  echo "Cached dependencies are restored to $CACHE_DIR_PATH"

else
  touch $CACHE_FLAG_PATH

  if (( $TIMESTAMP == 0 )); then
    echo "Skipping cache restore. Timestamp not found."
  else
    echo "Skipping cache restore. Timestamp is older than a month."
  fi
fi
