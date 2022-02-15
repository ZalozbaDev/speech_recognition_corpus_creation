#!/bin/bash

cd "${0%/*}"

python3 BASgenerator.py HSB.yaml

rm -f /results/*
cp uasr_configurations/lexicon/hsb_sampa.lex /results/
