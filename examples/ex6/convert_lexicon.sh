#!/bin/bash

(cat output/hsb_sampa.ulex | sed -e 's/^/LEX: /') > lexicon.lex

