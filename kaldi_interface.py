import subprocess
import os
from os import listdir
from os.path import isfile, join

def speechToText(file):
    """
    ############################################################################
    # Function Name: speechToText
    #
    # Input:         Full Path to Audio File (String)
    #
    # Output:        Transcription of Audio File (String)
    #
    # Dependencies:  ffmpeg, c++, kaldi (trained), python
    #
    # Description:   Jeffery has a terrible memory so he always records his
    #                interviews with his phone. Unfortunately, relistening to an
    #                old interview takes ages (0.1 - 2 hours). To make his life
    #                easier, he now just reads the transcription rather than
    #                listening to the audio. Eventually, he'd like a robot to do
    #                that portion too and just give him a tl;dr. 
    #
    # Example Usage: import kaldi_interface as ki
    #                my_transcription = ki.speechToText("path_to_audio_file.xy")
    #
    # Notes:         For large audio files this can take quite a while. Please
    #                be patient. Also, please do not make any modifications to
    #                any of the directory structure or beam parameters. 
    #                
    # Technique:     We use python as an interface to call bash commands and 
    #                scripts to work with the c++ software. ffmpeg is used for
    #                audio conversion and downsampling. Sphinx is used for 
    #                mfcc extraction as well as delta and delta delta features.
    #                A time delay neural network (chained with frame decimation) 
    #                is used inside of a hidden markov model as an acoustic 
    #                model and then fed to a Bi-directional LSTM for language 
    #                modeling. 
    #
    ############################################################################
    """
    
    path_to_decoder = "/usr/local/kaldi/egs/aspire/s5"
    path_to_text    = "/usr/local/audio_text"
    temp_folder     = "/usr/local/kaldi/egs/aspire/s5/tmp"
    orig_dir = os.getcwd()
    
    #navigate to decoder directory to set up environment
    os.chdir(path_to_decoder)
    
    #downsample and convert file
    if not os.path.isdir(temp_folder):
        os.makedirs(temp_folder)
    
    if not os.path.exists(file):
        #print("Path to audio file incorrect")
        raise Exception("Path to audio file incorrect")
        return 
        
    conversion_command = "ffmpeg -i "+ \
                          file       + \
                          " -acodec pcm_s16le -ac 1 -ar 8000 "+ \
                          temp_folder +\
                          "/downsampled.wav"
    try:
        subprocess.run(conversion_command, shell=True)
    except:
        raise Exception("Audio Conversion Failed.")
        return
    
    
    
    #decode audio file
    decode_commands =   "sh decode_interface.sh " +\
                        temp_folder +\
                        "/downsampled.wav"
    try:                    
        dirty_transcript = subprocess.check_output([decode_commands],\
                                                    cwd = path_to_decoder,\
                                                    shell = True, \
                                                    stderr = subprocess.STDOUT)
    except:
        raise Exception("Audio Decoding Failed.")
        return
    
    #parse log for transcription
    transcript = ""
    try:
        for line in dirty_transcript.decode('UTF-8').split('\n'):
            if line[:13] == 'utterance-id1':
                transcript = line[13:]
                break
    except:
        raise Exception("Parsing of Transcript Logs Failed")
        return

    #clean up temp files
    os.remove(temp_folder+"/downsampled.wav")
    
    #exit gracefully
    return transcript
    
def speechToTextTest():
    """
    ############################################################################
    # Function Name: speechToTextTest
    #
    # Input:         N/A
    #
    # Output:        N/A
    #
    # Dependencies:  ffmpeg, c++, kaldi (trained), python
    #
    # Description:   Alfred just got this new speechToText library but he can't
    #                get the darned thing to work! He's not sure if it's him
    #                or if the library itself is broken. He can run this 
    #                function to easily test if the library works.
    #
    # Example Usage: import kaldi_interface as ki
    #                my_transcription = ki.speechToTextTest()
    #
    # Notes:         This should only take a couple minutes max. It will print
    #                quite a bit but the final statement will be 
    #                "All Tests Successful"
    #                If it doesn't work out, your directory structure or
    #                installation may be corrupted. Try a fresh install of the 
    #                original docker. 
    #                
    ############################################################################
    """
    path_to_audio   = "/usr/local/test_audio"
    transcript = speechToText(path_to_audio+"/short_sample.m4a")
    print("\n\nTest Transcription:\n\n")
    print(transcript)
    print("\n\n All Tests Successful")

def speechToTextBatch(in_folder = '/usr/local/audio_files', \
                      out_folder = '/usr/local/audio_text'):
    """
    ############################################################################
    # Function Name: speechToTextBatch
    #
    # Input:         Full Path to Folder Containing Audio Files (String)
    #
    # Output:        Transcription of Audio Files (List of Strings)
    #                Transcription of Audio Files (Folder of Text Files)
    #
    # Dependencies:  ffmpeg, c++, kaldi (trained), python
    #
    # Description:   Jimbo Jenkins wants to transcribe some audio but he barely
    #                knows any python! His intern knows even less! It'd be 
    #                pretty great if they could just drag and drop some files
    #                into a folder and just call a function that would give him
    #                text files. That's exactly what this function does.
    #
    # Example Usage: import kaldi_interface as ki
    #                ki.speechToTextBatch()
    #
    # Notes:         All audio files should be placed in the "audio_files" 
    #                folder. You can override the folder location as an argument
    #                but you don't have to. There is also a default output 
    #                folder but you can override it if you'd like. This will 
    #                probably take a while to process. Just let it run,
    #                kick back, and relax.    
    #
    ############################################################################
    """
    
    if not os.path.isdir(in_folder):
        raise Exception("Input Folder does not exist or cannot be found")
        return 
    if not os.path.isdir(out_folder):
        os.makedirs(out_folder)
    
    #clear output folder
    for the_file in os.listdir(out_folder):
        file_path = os.path.join(out_folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            raise Exception(e)
            return 
    
    #Get Path of Every File in Folder
    files = [f for f in listdir(in_folder) if isfile(join(in_folder, f))]
    
    transcriptions_list = []
    #for each file, get a transcription and then save it to a text file
    for audio_file in files:
        
        #get transcript
        try: 
            transcription = speechToText(in_folder+'/'+audio_file)
            #append to list
            transcriptions_list.append([audio_file,transcription])
            #save transcription to file
            fname = out_folder+"/"+audio_file.split('.')[0]+'.txt'
            textfile = open(fname,'w')
            textfile.write(transcription)
            textfile.close()
        except:
            raise Exception("Transcription failed for file "+audio_file)  
    
    #exit gracefully
    return transcriptions_list
    
def speechToTextBatchTest():
    """
    ############################################################################
    # Function Name: speechToTextBatchTest
    #
    # Input:         N/A
    #
    # Output:        List of lists [name, transcription]
    #                Transcriptions by name (text files)
    #
    # Dependencies:  ffmpeg, c++, kaldi (trained), python
    #
    # Description:   Jennifer wants to try using this speechToText software and
    #                she put all her audio files into some folder and clicked 
    #                run. But like usual, it didn't work. It just spit out weird
    #                things the local IT guy called "error messages". Run this 
    #                function to see if Jennifer ran the script incorrectly or
    #                if the actual functionality is broken
    #
    # Example Usage: import kaldi_interface as ki
    #                test = ki.speechToTextBatchTest()
    #                print(test)
    #
    # Notes:         This should take 5-10 minutes.    
    #
    ############################################################################
    """
    
    infolder_test  = "/usr/local/test_audio"
    outfolder_test = "/usr/local/test_text"
    
    transcriptions_list =  speechToTextBatch(in_folder = infolder_test, \
                        out_folder = outfolder_test)
    print("\n\nAll Tests Successful")
    return transcriptions_list