#!/bin/bash
conda deactivate
mkdir -p aws-layer2/python/lib/python3.7/site-packages
pip3 freeze > requirements.txt
pip3 install -r requirements.txt --target aws-layer/python/lib/python3.7/site-packages
cd aws-layer2
zip -r lambda-layer.zip .