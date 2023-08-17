# Corpus generation tooling manual

## Configuration (.yaml)

- You can specify as many texts as you like in "input_txts:".
- You can supply custom lexika which are used without processing at "hcraft_lex:". 
Put foreign words there, and other words that are special.
- Take care to specify all digraphs!
- TBD reduction of phonetic inventory?

## Phoneme inventory

Syntax:

```code
grapheme <TAB> default phoneme/symbol <TAB> properties
```

Examples:

```code
Č	tS	C
O	O	V
```

Properties are:
- C (consonant)
- V (vowel)
- S (TBD?)

You can also remap a grapheme to more than one symbol by separating them with space.

Examples:

```code
X	k s	C
Q	k w	C
```

## Exception rules

Syntax:

```code
matcher <TAB> phoneme(s)/symbol(s) <TAB> rule type <TAB> comments (ignored)
```

Examples:

```code
; this is a comment line
P_Ě_Š	1	ALTERNATIVE	spěšnje
$_CH_L	k	MANDATORY	CHLĚB, CHLĚWJE (dito)
```

### Matcher

```code
[PREDECESSOR]_GRAPHEME_[SUCCESSOR]
```

- PREDECESSOR and SUCCESSOR special symbols:
    - #C - all consonants
    - #V - all vowels
    - $ - word boundary (start resp end of word) 
- PREDECESSOR and SUCCESSOR can be left out
    - this is the equivalent to having 2 rules with both "#C" and "#V" instead

### Phonemes/Symbols

Either one symbol or a list of options:

Examples:

```code
N_J_E	(j|*)	MANDATORY	njebjeskim, njetrjebać, njecha, njeplech (j --> *)
```

## Rule type

- MANDATORY: delete the original line/the default pronunciation
- ALTERNATIVE: keep the original line/the default pronunciation and add a new line with this/these option(s)

