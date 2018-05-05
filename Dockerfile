FROM ubuntu:16.04

MAINTAINER sih4sing5hong5

ENV CPU_CORE 4

RUN \
  apt-get update -qq && \
  apt-get install -y \
    git bzip2 wget \
    g++ make python python3 \
    zlib1g-dev automake autoconf libtool subversion \
    libatlas-dev libatlas-base-dev


WORKDIR /usr/local/
# Use the newest kaldi version
RUN git clone https://github.com/kaldi-asr/kaldi.git


WORKDIR /usr/local/kaldi/tools
RUN extras/check_dependencies.sh
RUN make -j $CPU_CORE

WORKDIR /usr/local/kaldi/src
RUN ./configure && make depend -j $CPU_CORE && make -j $CPU_CORE

RUN rm /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python

RUN cd /usr/local/kaldi/egs/aspire/s5 && \
    wget http://dl.kaldi-asr.org/models/0001_aspire_chain_model.tar.gz && \
    tar xfv 0001_aspire_chain_model.tar.gz && \
    chmod +x steps/online/nnet3/prepare_online_decoding.sh && \
    chmod +x utils/mkgraph.sh && \
    steps/online/nnet3/prepare_online_decoding.sh --mfcc-config conf/mfcc_hires.conf data/lang_chain exp/nnet3/extractor exp/chain/tdnn_7b exp/tdnn_7b_chain_online && \
    utils/mkgraph.sh --self-loop-scale 1.0 data/lang_pp_test exp/tdnn_7b_chain_online exp/tdnn_7b_chain_online/graph_pp

RUN apt-get install -y software-properties-common && \
    add-apt-repository ppa:mc3man/xerus-media && \
    apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get install -y frei0r-plugins

RUN mkdir -p /usr/local/audio_files && \
    mkdir -p /usr/local/audio_text && \
    mkdir -p /usr/local/test_audio && \
    mkdir -p /usr/local/test_text

ADD decode_interface.sh /usr/local/kaldi/egs/aspire/s5/
RUN chmod +x /usr/local/kaldi/egs/aspire/s5/decode_interface.sh
RUN chmod +x /usr/local/kaldi/egs/aspire/s5/cmd.sh
ADD kaldi_interface.py /usr/local/
ADD short_sample.m4a /usr/local/test_audio
ADD short_sample2.m4a /usr/local/test_audio
