# $1 is the filepath to the audio file

. /user/local/kaldi/egs/aspire/s5/cmd.sh
. /user/local/kaldi/egs/aspire/s5/path.sh
online2-wav-nnet3-latgen-faster   --online=false   --do-endpointing=false   --frame-subsampling-factor=3   --config=/user/local/kaldi/egs/aspire/s5/exp/tdnn_7b_chain_online/conf/online.conf   --max-active=7000   --beam=15.0   --lattice-beam=6.0   --acoustic-scale=1.0   --word-symbol-table=/user/local/kaldi/egs/aspire/s5/exp/tdnn_7b_chain_online/graph_pp/words.txt   exp/tdnn_7b_chain_online/final.mdl   exp/tdnn_7b_chain_online/graph_pp/HCLG.fst   'ark:echo utterance-id1 utterance-id1|'   "scp:echo utterance-id1 $1|"   'ark:/dev/null'
