import subprocess
import os
from os import listdir
from os.path import isfile, join

path_to_audio = "/usr/local/audio_files"

def speechToText(file):
    orig_dir = os.getcwd()
    
    path_to_decoder = "/usr/local/kaldi/egs/aspire/s5"
    path_to_audio   = "/usr/local/audio_files"
    path_to_text    = "/usr/local/audio_text"

    os.chdir(path_to_decoder)

    decode_commands = "sh decode_test.sh " + path_to_audio + "/" + file
	print()
    print("Processing...")
	print()
    dirty_transcript = subprocess.check_output([decode_commands],cwd = path_to_decoder, shell = True, stderr = subprocess.STDOUT)

    transcript = ""
    for line in dirty_transcript.decode('UTF-8').split('\n'):
        if line[:13] == 'utterance-id1':
            transcript = line[13:]
            textfile = open(path_to_text + "/" + os.path.splitext(os.path.basename(file))[0] + ".txt", 'w')
            textfile.write(transcript)
            textfile.close()
            print("Text outputed as " + path_to_text + "/" + os.path.splitext(os.path.basename(file))[0] + ".txt")
			print()
            break

onlyfiles = [f for f in listdir(path_to_audio) if isfile(join(path_to_audio, f))]

for i in onlyfiles:    
    print(i)
    speechToText(i)
	