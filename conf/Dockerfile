# Copyright 2014-16 Joseph Wolff & The Libre Group

FROM ubuntu:xenial
#FROM ubuntu:trusty

MAINTAINER Joseph Wolff, joe@eracks.com

ENV TERM linux

#RUN locale-gen en_US.UTF-8
#RUN update-locale LANG=en_US.UTF-8

RUN echo Running apt-get update

RUN apt-get -y update

ADD install-packages.sh .
RUN bash install-packages.sh
RUN wget --version

ADD requirements.txt .
RUN pip install -r requirements.txt

RUN npm -g install stylus bower

RUN ls -l

EXPOSE 8000
# 22 2222 80 8080 443

# Note: you MUST use double-quotes here in both of these:
ENTRYPOINT ["/bin/bash", "-i"]
#CMD ["setup-envo.sh"]

