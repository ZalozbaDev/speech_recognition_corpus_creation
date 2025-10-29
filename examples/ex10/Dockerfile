FROM debian:bullseye-slim
MAINTAINER Daniel Sobe <daniel.sobe@sorben.com>

# normal call
# docker build --progress=plain -t speech_recognition_corpus_creation_ex10 .

# rebuild from scratch
# docker build -t speech_recognition_corpus_creation_ex10 . --no-cache

# enable in case you want to install tools from contrib or non-free
# RUN sed -i 's/ main/ main contrib non-free/' /etc/apt/sources.list

RUN apt update

# generic tools install 
RUN apt install -y g++ make git procps nano

############################################
# Generate "classes.txt" file from scratch
############################################

# install tools for running "BASgenerator.py"
RUN apt install -y python3 python3-numpy python3-matplotlib python3-yaml

RUN mkdir -p configuration
RUN mkdir -p resources
RUN mkdir -p tooling
RUN mkdir -p results

COPY configuration configuration
COPY resources resources
COPY tooling tooling
COPY runme.sh /

RUN chmod 755 /runme.sh && /runme.sh

#############################################
#
# fetch results
#
#############################################

# rm -rf output && mkdir -p output
# docker run --mount type=bind,source="$(pwd)"/output,target=/results/ -it speech_recognition_corpus_creation_ex10 cp -r /output/ /results




