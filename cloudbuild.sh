#!/bin/sh

echo "Build process started..."
echo PORT=8080 > .env
echo PROD_PYTHON_SCRIPT="~/markets/app/python/index.py" >> .env
mkdir markets
mv *[^markets] ./markets
# cp -r *[^markets] ./markets
# cp -r ./* ./markets