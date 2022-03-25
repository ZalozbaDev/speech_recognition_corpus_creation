#!/bin/bash

# Source directory with files to analyze
InDir=$1

find $InDir -regex '.*\.\(mp3\|wav\)' -type f -print0 | while read -d $'\0' input
do
  #echo $input
 	
  D=$(soxi -D $input)
  d=$(soxi -d $input)
  sample_rate=$(soxi -r $input)
  bit_sample=$(soxi -b $input)	
  channels=$(soxi -c $input)	
  encoding=$(soxi -e $input)	
  prms=$(sox $input -n stats 2> >(grep 'RMS Pk dB') | rev | cut -d ' ' -f 1 | rev)
  trms=$(sox $input -n stats 2> >(grep 'RMS Tr dB') | rev | cut -d ' ' -f 1 | rev)
  voladj=$(sox $input -n stat 2> >(grep 'Volume adjustment') | rev | cut -d ' ' -f 1 | rev)
  pcount=$(sox $input -n stats 2> >(grep 'Pk count') | rev | cut -d ' ' -f 1 | rev)
  flat=$(sox $input -n stats 2> >(grep 'Flat factor') | rev | cut -d ' ' -f 1 | rev)

  echo $input$'\t'$D$'\t'$d$'\t'$prms$'\t'$trms$'\t'$voladj$'\t'$pcount$'\t'$flat$'\t'$sample_rate$'\t'$bit_sample$'\t'$channels$'\t'$encoding
done