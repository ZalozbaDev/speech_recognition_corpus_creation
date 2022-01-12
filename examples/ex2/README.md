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
- **sorbian_institute_monolingual.hsb**		Upper Sorbian monolingual data provided by the Sorbian Institute (contains a high quality corpus and some medium quality data which are mixed together) - downloaded and extracted upon container creation
- **web_monolingual.hsb**					Upper Sorbian monolingual data scraped from the web by CIS, LMU (thanks to Alina Fastowski). Use with caution, probably noisy, might erroneously contain some data from related languages - downloaded and extracted upon container creation
- **witaj_monolingual.hsb**					Upper Sorbian monolingual data provided by the Witaj Sprachzentrum (high quality) - downloaded and extracted upon container creation

## Grapheme and Phoneme Inventory and G2P mappings
- **phonmap.txt**							phoneme inventory (grapheme, phoneme, (C)onsonant or (V)owel)
- **exceptions_v2.txt**						G2P rules version 2 (derived from available lexicons)
