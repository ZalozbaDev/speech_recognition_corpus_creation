#!/bin/bash

rm -rf output/
pushd tooling
python3 corpus_creator.py ../configuration/DSB.yaml
popd
