# Generator for BAS projects

The script generate BAS speechrecorder project along with textual data necessary for language modeling. 

	python3 BASgenerator.py HSB.yaml

## Script
The working directory contain the following files that are input for the script:

- **BASgenerator.py**	python (3.7) script for corpus normalization, lexicon generation and prompts selection.
- **HSB.yaml**			configuration file (YAML).

## Textual Corpus
- **cv.hsb**								Common Voice Texts - provided
- **smartlamp.hsb**							Textual data from the "SmartLamp" domain - provided

## Grapheme and Phoneme Inventory and G2P mappings
- **phonmap.txt**							phoneme inventory (grapheme, phoneme, (C)onsonant or (V)owel)
- **exceptions_v1.txt**						G2P rules version 1 (based on the "Obersorbisch -Aus der Perspektive der slavischen Interkomprehension")
