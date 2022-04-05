#!/bin/bash
deactivate # deactivate the venv
cd venv/lib/python3.7/site-packages 
zip -r ../../../../my-deployment-package.zip .
cd ../../../../gmail_spam/src
zip -g ../../my-deployment-package.zip lambda_fn.py

aws lambda publish-layer-version \
    --layer-name gmail-spam-layer \
    --description "My Python layer" \
    --zip-file fileb://lambda-layer.zip \
    --compatible-runtimes python3.7