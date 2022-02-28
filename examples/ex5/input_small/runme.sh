#!/bin/bash

cd "${0%/*}"

python3 BASgenerator.py HSB_small.yaml

rm -f /results/*
cp uasr_configurations/lexicon/hsb_small_sampa.lex /results/
