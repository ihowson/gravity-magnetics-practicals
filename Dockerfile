FROM ubuntu:trusty

MAINTAINER Ian Howson

RUN apt-get update -y

RUN apt-get install -y python-pip

RUN pip install -U setuptools
RUN pip install -U pip  # fixes AssertionError in Ubuntu pip
RUN pip install jupyter matplotlib
RUN pip install scipy
RUN pip install numpy

# Add Tini

RUN whoami

ENV TINI_VERSION v0.8.4
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/local/bin/tini
RUN chmod +x /usr/local/bin/tini

RUN mkdir /workspace && \
    mkdir /workspace/volume

# copy labs
COPY content/ /workspace/

# expose notebook port
EXPOSE 8888

# setup space for working in
VOLUME /workspace/volume

# launch notebook
WORKDIR /workspace
EXPOSE 8888
ENTRYPOINT ["/usr/local/bin/tini", "--"]

CMD jupyter notebook --ip=0.0.0.0 --no-browser \
    --NotebookApp.default_url='/notebooks/StartHere.ipynb'

