FROM debian:bullseye-slim
MAINTAINER Daniel Sobe <daniel.sobe@sorben.com>

# normal call
# docker build -t speech_recognition_corpus_creation_ex7 .

# rebuild from scratch
# docker build -t speech_recognition_corpus_creation_ex7 . --no-cache

RUN apt update

RUN apt install -y python3 python3-numpy python3-matplotlib python3-yaml

RUN mkdir -p /output/
RUN mkdir -p /input/

COPY input/tooling/*       /input/
COPY input/configuration/* /input/
COPY input/scripts/*       /input/
COPY input/resources/*     /input/

# tools for inspecting container
RUN apt install -y procps nano

# just a default instruction, might be handy
CMD ["/bin/bash"]

# how to use this container to run the tool:
## mkdir -p output && rm -rf ./output/* 
## docker run --mount type=bind,source="$(pwd)/output",target=/output/ -it speech_recognition_corpus_creation_ex7 /input/runme.sh


