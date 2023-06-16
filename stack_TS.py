import sys
import numpy as np
import wave
from PIL import Image
import os
import glob
import csv

# Stack the tones into a single image
indir = "./TS/" # directory containing the training data
testdir = "./TEST/" # directory containing the test data
outdir = "./stacked_sets/" # directory to store the stacked tones


patterns = {
    "0": indir + "0_" + "*.wav",
    "1": indir + "1_" + "*.wav",
    "2": indir + "2_" + "*.wav",
    "3": indir + "3_" + "*.wav",
    "4": indir + "4_" + "*.wav",
    "5": indir + "5_" + "*.wav",
    "6": indir + "6_" + "*.wav",
    "7": indir + "7_" + "*.wav",
    "8": indir + "8_" + "*.wav",
    "9": indir + "9_" + "*.wav",
    "A": indir + "A_" + "*.wav",
    "B": indir + "B_" + "*.wav",
    "C": indir + "C_" + "*.wav",
    "D": indir + "D_" + "*.wav",
    "pound": indir + "pound_" + "*.wav",
    "star": indir + "star_" + "*.wav"
}

training_files_list = []
testing_files_list = []
for pattern in patterns.values():
    files = glob.glob(pattern)
    files.sort()
    training_files_list.append(files)
    pattern = pattern.replace(indir, testdir)
    files = glob.glob(pattern)
    files.sort()
    testing_files_list.append(files)

# print(files_list[0])

def create_map(indir, outdir):
    """
    Create a mapping of input files to output files

    Parameters
    ----------
    indir : string
        The directory containing the input files
    outdir : string
        The directory containing the output files

    Returns
    -------
    mapping : dictionary
        Maps the input files to the output files
    """
    mapping = {}
    characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "pound", "star"]

    for character in characters:
        pattern = indir + character + "_*.wav"
        outfile = outdir + "ts_" + character + ".dat"
        mapping[pattern] = outfile
    
    return mapping

def stack_tones(files_list, mapping, test=False):
    """
    Stack the tones into a single file

    Parameters
    ----------
    files_list : a list of lists of files
        Each list contains the files for a single character
    mapping : a dictionary
        Maps the input files to the output files
    """
    for i, files in enumerate(files_list):
        ts_infile = files[0].replace("\\", "/")
        ts_infile = ts_infile.replace("001", "*")
        ts_outfile = mapping.get(ts_infile)
        if test:
            ts_outfile = ts_outfile.replace("ts_", "test_")
        dat_file = open(ts_outfile, "wb")
        # open csv file for writing
        # csv_outfile = ts_outfile.replace(".dat", ".csv")
        # csv_file = open(csv_outfile, "w")
        # writer = csv.writer(csv_file)
        for i, infile in enumerate (files):
            infile = infile.replace("\\", "/")
            print(f"Processing {infile}")
            with wave.open(infile, 'r') as f:
                frames = f.readframes(-1)
                tone = np.frombuffer(frames, dtype=np.int16)
                tone.tofile(dat_file)
                # writer.writerow(tone)
                # if i == 0:
                #     print(tone)
                #     # print(tone_arr)
                #     # print(f"Length of tone_arr: {len(tone_arr)}")  
                #     break
        # if i==0:
        #     break     
        dat_file.close()
        

# Stack the training tones
mapping = create_map(indir, outdir)
stack_tones(training_files_list, mapping)

# Stack the testing tones
mapping = create_map(testdir, outdir)
stack_tones(testing_files_list, mapping, test=True)