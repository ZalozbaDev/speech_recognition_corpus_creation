#!/bin/bash

cd /input/ 
python3 corpus_creator.py TEST.yaml

cp -r corpus uasr_configurations /output/
