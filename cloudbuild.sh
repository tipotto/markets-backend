#!/bin/sh

# DIR=api
echo "Build process started..."
echo PORT=8080 >> .env
echo PROD_PYTHON_SCRIPT="~/api/app/python/index.py" >> .env
# .env > /workspace/
mkdir api
mv .env ./api
mv *[^api] ./api
ls -l
# ls *[^markets] | xargs mv -t ./markets
# chown -R tipotto404:tipotto404 ./markets
# cp -r *[^markets] ./markets
# cp -r ./* ./markets