import subprocess
import os
orig_dir = os.getcwd()
path_to_decoder = "/usr/local/kaldi/egs/aspire/s5"
path_to_wav_file = "/usr/local/kaldi/egs/aspire/s5/short_sample.wav"
os.chdir(path_to_decoder)
decode_commands = "sh decode_test.sh " + path_to_wav_file
dirty_transcript = subprocess.check_output([decode_commands],cwd=path_to_decoder, shell=True, stderr=subprocess.STDOUT)#,check=True)
transcript = []
for line in dirty_transcript.decode('UTF-8').split('\n'):
    if line[:13]=='utterance-id1':
        transcript.append(line[13:])
#go back to original path
os.chdir(orig_dir)