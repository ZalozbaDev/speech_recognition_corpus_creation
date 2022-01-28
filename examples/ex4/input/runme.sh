#!/bin/bash

cd "${0%/*}"

python3 BASgenerator.py HSB.yaml

rm -f /results/*
cp corpus/hsb_sampa.lex /results/

