#!/bin/bash
# save-cache: Save the npm cache to GCS.
# $npm_cache = /home/cache/.npm
# cloudbuildのボリューム（$npm_cache）からファイルをコピー
# コピーしたファイルをtgz形式で圧縮
# GCSのバケットにtgzファイルをコピー
# GCSのバケットにタイムスタンプをコピー

set -e -u

echo "Working dir: $(pwd)"

if [ -e $CACHE_FLAG_PATH ]; then
  tar -czf /tmp/npm.tgz -C ./api/node_modules .
  echo "Cached dependencies are copied from $CACHE_DIR_PATH"

  echo "Saving dependencies to gs://$CACHE_BUCKET_NAME/"
  gsutil -q -m cp /tmp/npm.tgz gs://$CACHE_BUCKET_NAME/
  
  echo "Saving timestamp to gs://$CACHE_BUCKET_NAME/timestamp"
  date +%s | gsutil -q cp - gs://$CACHE_BUCKET_NAME/timestamp
fi