FROM debian:bullseye-slim
MAINTAINER Daniel Sobe <daniel.sobe@sorben.com>

# normal call
# docker build -t speech_recognition_corpus_creation_ex5 .

# rebuild from scratch
# docker build -t speech_recognition_corpus_creation_ex5 . --no-cache

RUN sed -i 's/ main/ main contrib non-free/' /etc/apt/sources.list

RUN apt update

RUN apt install -y python3 python3-numpy python3-matplotlib python3-yaml

RUN mkdir -p /results/
RUN mkdir -p /input/

# tools for "reading out" lexicon entries
RUN apt install -y mbrola-de6 alsa-utils libterm-readkey-perl

ADD read_lexicon.pl /

# tools for inspecting container
RUN apt install -y procps nano

# just a default instruction, might be handy
CMD ["/bin/bash"]

# how to use this container to run the tool:
## mkdir -p output && rm -rf ./output/* 
## docker run --mount type=bind,source="$(pwd)"/output,target=/results/ --mount type=bind,source="$(pwd)"/input,target=/input/ -it speech_recognition_corpus_creation_ex5 /input/runme.sh
# read out lexicon
## docker run --privileged --mount type=bind,source="$(pwd)"/output,target=/results/ -it speech_recognition_corpus_creation_ex5 /read_lexicon.pl /results/hsb_sampa.lex de6

# alternative run for a smaller lexicon (adaptation)
## mkdir -p output_small && rm -rf ./output_small/* 
## docker run --mount type=bind,source="$(pwd)"/output_small,target=/results/ --mount type=bind,source="$(pwd)"/input_small,target=/input/ -it speech_recognition_corpus_creation_ex5 /input/runme.sh

# on windows, assure runme.sh is converted to unix linefeeds, and run a cmdline similar to this one (replace absolute paths):
##  winpty docker run --mount type=bind,source="/c/Users/$USER/$PATH_TO_HERE/output",target=/results/ --mount type=bind,source="/c/Users/$USER/$PATH_TO_HERE/input",target=/input/ -it speech_recognition_corpus_creation_ex5
## at the prompt:
## cd /input
## ./runme.sh
