#!/bin/bash

cd "${0%/*}"

cp /sorbian_institute_monolingual.hsb /witaj_monolingual.hsb /web_monolingual.hsb /input

python3 BASgenerator.py HSB.yaml

mv corpus/ sentences/ speechrecorder/ transliterations/ /results/

echo "Please add the file 'SpeechRecPrompts_4.dtd' manually to every Speechrecorder project!"
echo "Either take the one that is checked in, or let Speechrecorder create a new one when creating a new project."
