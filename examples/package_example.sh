#!/bin/bash

rm -rf corpus_creator/ corpus_creator.zip
mkdir corpus_creator

cp README.manual.md corpus_creator

rm -rf ex8/output/
rm -rf ex8/tooling/__pycache__/

cp -r ex8/* corpus_creator

zip -r corpus_creator.zip corpus_creator

