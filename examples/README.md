# Examples

## Overview

- ex1: Uses MIT licensed corpora and G2P rules from the 2020 study project. Processing is fast.

- ex2: Uses corpora from ex1 plus more corpora which are downloaded, and newer G2P rules. Takes quite a while to process.

- ex3: Uses MIT licensed corpora and custom G2P rules. No sentence selection. Processing is fast.

- ex4: Uses MIT licensed smartlamp corpora and custom G2P rules. No sentence selection. Processing is fast.

- ex5: Uses most recent scripts, MIT licensed corpora and most recent phoneme map and G2P rules. Recommended! Processing is fast.

### Hints

If sentence selection is not needed, turn it off to get the normalized corpus, the vocabulary and the lexicon only. Change

    basic_type: "diphones"      # "phones", "diphones", "triphones" or empty not generating sentences
    to 
    basic_type:       # "phones", "diphones", "triphones" or empty not generating sentences

to achieve this.

## Running

The examples have been tested on Linux and Windows on x86_64 architecture using Docker. 
Please check the comments in the "Dockerfile" of each example to see how the container is build and how to run the processing.

## Results

The results of the script are described in the report, chapter 2.4.
