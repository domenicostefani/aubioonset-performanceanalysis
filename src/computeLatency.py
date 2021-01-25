#!/usr/bin/env python3

## Compute the AUBIOONSET delay with different parameters
#
# ** This is intended to be used with different support script
#    and placed in its original repository directory.
#
# This script does multiple things:
# - It asks the user for the parameters for AUBIOONSET
# - It calls "extractAllOnsets.sh" with those parameters, which calls aubioonset
#   on all the WAV files in the folder
# - It compares the onsets labeled with the ones extracted
#   When computing the delay, it sums the delay value that AUBIOONSET regularly
#   subtracts to the detection time, to center the distribution around 0
# - It finally calls a R analysis script to plot the delay distribution and the
#   metrics (Accuracy, Precision, Recall)
#
# Author: Domenico Stefani
#         domenico.stefani[at]unitn.it
#         domenico.stefani96[at]gmail.com
# Date:   10th Nov 2020
#
##

import glob             # To read folder filelist
import os               # To call scripts
import re               # Regexp, to parse script results
from enum import Enum   # To specify parameter type
import sys

DEF_BUFFERSIZE = -1 
DEF_METHOD = ""
if len(sys.argv) == 2:
    DEF_METHOD = sys.argv[1]
elif len(sys.argv) == 3:
    DEF_METHOD = sys.argv[1]
    DEF_BUFFERSIZE = sys.argv[2]
elif len(sys.argv) > 3:
    print("Too many arguments")
    exit(-1)


# *Main comparation hyperparameter*
# This states the maximum time delay between labeled and detected onset
# in order for them to be considered the same onset
# Onsets further apart than this interval will be considered different
MAX_ONSET_DIFFERENCE_S = 0.02
print("Onset further apart than " + str(MAX_ONSET_DIFFERENCE_S*1000.0) + \
      "ms are considered different")
IGNORE_NEG = True

class ParamType(Enum):  # Aubioonset parameter type
    INT = 1
    FLOAT = 2
    STR = 3

# Ask the user to input the parameter, or use default if none is specified
def readParam(param_name,default_value,param_type):
    try:
        param_str = input(param_name+"(default: " + str(default_value) + "): ")
        if param_str is not "":
            if param_type is ParamType.INT:
                param_val = int(param_str)
            elif param_type is ParamType.FLOAT:
                param_val = float(param_str)
            elif param_type is ParamType.STR:
                param_val = param_str
            else:
                print("ERROR! Wrong parameter type")
                exit()
        else:
            param_val = default_value;
            print("Using default value for " + param_name + " (" + str(default_value) + ")")
        return param_val
    except ValueError:
        print("ValueError")


# Read all the parameters
print("Extracting all the onsets from the wav files in this folder")
print("Specify the parameter values or press <ENTER> for default")
if DEF_BUFFERSIZE == -1:
    BUFFER_SIZE = readParam("BUFFER_SIZE",64,ParamType.INT)
else:
    BUFFER_SIZE = DEF_BUFFERSIZE
HOP_SIZE = 64#readParam("HOP_SIZE",64,ParamType.INT)
SILENCE_THRESHOLD = readParam("SILENCE_THRESHOLD",-48.0,ParamType.FLOAT)
ONSET_THRESHOLD = readParam("ONSET_THRESHOLD",0.75,ParamType.FLOAT)
if DEF_METHOD == "":
    print("Available methods:<default|energy|hfc|complex|phase|specdiff|kl|mkl|specflux>")
    ONSET_METHOD = readParam("ONSET_METHOD",DEF_METHOD,ParamType.STR)
else:
    ONSET_METHOD = DEF_METHOD
MINIMUM_INTER_ONSET_INTERVAL_SECONDS = 0.020 #readParam("MINIMUM_INTER_ONSET_INTERVAL_SECONDS",0.020,ParamType.FLOAT)

# Create the option string with the parameter values specified
opts = " -B " + str(BUFFER_SIZE) + \
       " -H " + str(HOP_SIZE) + \
       " -s " + str(SILENCE_THRESHOLD) + \
       " -t " + str(ONSET_THRESHOLD) + \
       " -O " + str(ONSET_METHOD) + \
       " -M " + str(MINIMUM_INTER_ONSET_INTERVAL_SECONDS) + \
       " -d " + "audiofiles/" + ""

# Call onset extraction routine
EXT_RES = os.popen("./utility_scripts/extractAllOnsets.sh " + opts).read()

# Parse script output, looking for the AUBIOONSET delay (in samples)
PARTIAL_STRING = re.search("To get the real detection time, add the delay of [0-9]+ samples",EXT_RES).group(0)
print("!! READ: '" + PARTIAL_STRING + "'")

AUBIODELAY_SAMPLES = int(re.search('[0-9]+', PARTIAL_STRING).group(0))

# To get the real detection time, add the delay of 550 samples

print("The delay introduced by aubioonset is " + str(AUBIODELAY_SAMPLES) + " samples")
SAMPLE_RATE = 48000
AUBIODELAY_S = AUBIODELAY_SAMPLES * 1.0 / SAMPLE_RATE
print("Delay in ms " + str(AUBIODELAY_S*1000.0))

# Strings for CSV separator and Not-a-Number values
SEP_STR = ","   # separator
NAN_STR = "NAN" # NaN

# Compare the onsets in @labels_file and @extracted_file, compute the delay and
# write the result as a CSV to out_file
def computeDifference(recording_name,labels_file,extracted_file,out_file):
    end_flag = False                     # termination flag
    lbl_line = labels_file.readline()    # read the very first line
    ext_line = extracted_file.readline() # read the very first line
    while not end_flag:
        if lbl_line is "" and ext_line is "": # Terminate when both are EOF
            end_flag = True
        else:
            # Convert to float or set to infinity if EOF
            lbl_value = float(lbl_line.split()[0] if (lbl_line is not "") else "inf")
            ext_value = float(ext_line.split()[0] if (ext_line is not "") else "inf")
            # Compute the delay in seconds and sum AUBIOONSET delay
            diff = ext_value - lbl_value + AUBIODELAY_S
            # Skip values if onsets are different (delay greater than threshold)
            if abs(diff) < MAX_ONSET_DIFFERENCE_S and (not IGNORE_NEG or diff > 0):
                out_file.write(str(lbl_value) + SEP_STR + str(ext_value) + SEP_STR + str(diff) + SEP_STR + recording_name + "\n")
                lbl_line = labels_file.readline()
                ext_line = extracted_file.readline()
            elif lbl_value < ext_value:
                out_file.write(str(lbl_value) + SEP_STR + NAN_STR + SEP_STR + NAN_STR + SEP_STR + recording_name + "\n")
                lbl_line = labels_file.readline()
            elif lbl_value > ext_value:
                out_file.write(NAN_STR + SEP_STR + str(ext_value) + SEP_STR + NAN_STR + SEP_STR + recording_name + "\n")
                ext_line = extracted_file.readline()

# Print info
print("Computing the delays for:")
onsets_labeled = glob.glob("onsets_labeled/*.txt")
# Open output file
OUT_FILENAME="output/onset_delay.csv"
output_csv = open(OUT_FILENAME, "w")
# Write CSV header
output_csv.write("onset_labeled" + SEP_STR + "onset_extracted" + SEP_STR + "difference" + SEP_STR + "recording\n")

# Iterate over all label files and call computeDifference() for all files
for filename in onsets_labeled:
    filename = os.path.basename(filename)
    file_labels = open("onsets_labeled/"+filename, "r")
    file_extrac = open("onsets_extracted/"+filename, "r")
    computeDifference(filename,file_labels,file_extrac,output_csv)
    file_labels.close()
    file_extrac.close()

output_csv.close()

print("Output can be found at " + OUT_FILENAME)

# Call analysis script
print("Calling R analysis script")
logres_dir = "./results"
logres_filename = logres_dir+"/res_"+\
                  ONSET_METHOD+"_"+\
                  str(BUFFER_SIZE)+"_"+\
                  str(HOP_SIZE)+"_"+\
                  str(SILENCE_THRESHOLD)+"_"+\
                  str(ONSET_THRESHOLD)+"_"+\
                  str(MINIMUM_INTER_ONSET_INTERVAL_SECONDS)+".log"

os.system("mkdir -p "+logres_dir)
os.system("Rscript utility_scripts/r_analysis/analize_delays.r > "+logres_filename)

glob_metrics = dict.fromkeys(["accuracy","precision","recall","f1-score"])
for metric in glob_metrics.keys():
    glob_metrics[metric] = float(os.popen("cat " + logres_filename + '| grep -P \"\\\"'+metric+': [0-9]\.[0-9]+\\\"\"' + '| grep -P -o \"[0-9]\.[0-9]+\"').read())

macroavg_metrics = dict.fromkeys(["accuracy","precision","recall","f1-score"])
for metric in macroavg_metrics.keys():
    macroavg_metrics[metric] = float(os.popen("cat " + logres_filename + '| grep -P \"\\\"avg\_'+metric+': [0-9]\.[0-9]+\\\"\"' + '| grep -P -o \"[0-9]\.[0-9]+\"').read())

macroavg_tech_metrics = dict.fromkeys(["accuracy","precision","recall","f1-score"])
for metric in macroavg_tech_metrics.keys():
    macroavg_tech_metrics[metric] = float(os.popen("cat " + logres_filename + '| grep -P \"\\\"avg\_tech\_'+metric+': [0-9]\.[0-9]+\\\"\"' + '| grep -P -o \"[0-9]\.[0-9]+\"').read())

intensity_metrics = dict.fromkeys(["piano","mezzoforte","forte"])
for intensity in intensity_metrics.keys():
    intensity_metrics[intensity] = dict.fromkeys(["accuracy","precision","recall"])
    for metric in intensity_metrics[intensity].keys():
        intensity_metrics[intensity][metric] = float(os.popen("cat " + logres_filename + '| grep -P \"^'+intensity+"  "+metric+' [0-9]\.[0-9]+"' + '| grep -P -o \"[0-9]\.[0-9]+\"').read())

# Delay
adj_min = float(os.popen("cat " + logres_filename + '| grep -P -o \"\\[ [0-9]+\\.[0-9]+\"| grep -P -o \"[0-9]+\\.[0-9]+\"').read())
adj_max = float(os.popen("cat " + logres_filename + '| grep -P -o \", [0-9]+\\.[0-9]+ \\]ms\"| grep -P -o \"[0-9]+\\.[0-9]+\"').read())
avg = float(os.popen("cat " + logres_filename +     '| grep -P -o \"avg_delay:  \\d+\\.\\d+\"| grep -P -o \"\\d+\\.\\d+\"').read())
perc = float(os.popen("cat " + logres_filename +    '| grep -P -o \"[0-9]\\.[0-9]+  of the corr\"| grep -P -o \"[0-9]\\.[0-9]+\"').read())

output_string = ""
output_string += ONSET_METHOD+"\t"
output_string += str(BUFFER_SIZE)+"\t"
output_string += str(HOP_SIZE)+"\t"
output_string += str(MINIMUM_INTER_ONSET_INTERVAL_SECONDS)+"\t"
output_string += str(SILENCE_THRESHOLD)+"\t"
output_string += str(ONSET_THRESHOLD)+"\t \t"
output_string += "{:.4f}".format(glob_metrics["accuracy"])+"\t"
output_string += "{:.4f}".format(glob_metrics["precision"])+"\t"
output_string += "{:.4f}".format(glob_metrics["recall"])+"\t"
output_string += "{:.4f}".format(glob_metrics["f1-score"])+"\t"
output_string += " \t"
output_string += "{:.4f}".format(macroavg_metrics["accuracy"])+"\t"
output_string += "{:.4f}".format(macroavg_metrics["precision"])+"\t"
output_string += "{:.4f}".format(macroavg_metrics["recall"])+"\t"
output_string += "{:.4f}".format(macroavg_metrics["f1-score"])+"\t"
output_string += " \t"
output_string += "{:.4f}".format(macroavg_tech_metrics["accuracy"])+"\t"
output_string += "{:.4f}".format(macroavg_tech_metrics["precision"])+"\t"
output_string += "{:.4f}".format(macroavg_tech_metrics["recall"])+"\t"
output_string += "{:.4f}".format(macroavg_tech_metrics["f1-score"])+"\t"

output_string += " \t"
for intensity in intensity_metrics.keys():
    for metric in intensity_metrics[intensity].keys():
        output_string += "{:.4f}".format(intensity_metrics[intensity][metric])+"\t"
    output_string += "\t"



output_string += "{:.4f}".format(adj_min)+"\t"
output_string += "{:.4f}".format(avg)+"\t"
output_string += "{:.4f}".format(adj_max)+"\t"
output_string += "{:.4f}".format(perc)+"\t"
output_string += " \t"+logres_filename
print(output_string)

import pyperclip
pyperclip.copy(output_string)
spam = pyperclip.paste()


# Move plots to results folder
plots_suffix = logres_filename[:-4] + "_"
os.system("mv ./delay.pdf "+plots_suffix+"delay.pdf") 
os.system("mv ./metrics.pdf "+plots_suffix+"metrics.pdf") 
