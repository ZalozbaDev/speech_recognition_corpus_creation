FROM debian:bullseye-slim
MAINTAINER Daniel Sobe <daniel.sobe@sorben.com>

# normal call
# docker build -t speech_recognition_corpus_creation_ex2 .

# rebuild from scratch
# docker build -t speech_recognition_corpus_creation_ex2 . --no-cache

RUN apt update

RUN apt install -y python3 python3-numpy python3-matplotlib python3-yaml

RUN mkdir -p /results/
RUN mkdir -p /input/

# download & extract the additional corpora whose license is not clear
RUN apt install -y wget

RUN wget https://www.statmt.org/wmt20/unsup_and_very_low_res/sorbian_institute_monolingual.hsb.gz
RUN wget https://www.statmt.org/wmt20/unsup_and_very_low_res/witaj_monolingual.hsb.gz
RUN wget https://www.statmt.org/wmt20/unsup_and_very_low_res/web_monolingual.hsb.gz 

RUN gunzip sorbian_institute_monolingual.hsb.gz
RUN gunzip witaj_monolingual.hsb.gz
RUN gunzip web_monolingual.hsb.gz 

# just a default instruction, might be handy
CMD ["/bin/bash"]

# how to use this container to run the tool:
## mkdir -p output && rm -rf ./output/* 
## docker run --mount type=bind,source="$(pwd)"/output,target=/results/ --mount type=bind,source="$(pwd)"/input,target=/input/ -it speech_recognition_corpus_creation_ex2 /input/runme.sh


# on windows, assure runme.sh is converted to unix linefeeds, and run a cmdline similar to this one (replace absolute paths):
##  winpty docker run --mount type=bind,source="/c/Users/$USER/$PATH_TO_HERE/output",target=/results/ --mount type=bind,source="/c/Users/$USER/$PATH_TO_HERE/input",target=/input/ -it speech_recognition_corpus_creation_ex2
## at the prompt:
## cd /input
## ./runme.sh
