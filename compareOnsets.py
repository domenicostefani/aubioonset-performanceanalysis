#!/usr/bin/env python3

import glob
import os
import re

EXT_RES = os.popen("./extractAllOnsets.sh").read()

AUBIODELAY_SAMPLES = int(re.search('[0-9]+', EXT_RES).group(0))
print("AUBIODELAY_SAMPLES is " + str(AUBIODELAY_SAMPLES)) 
SAMPLE_RATE = 48000
AUBIODELAY_S = AUBIODELAY_SAMPLES * 1.0 / SAMPLE_RATE

MAX_ONSET_DIFFERENCE_S = 0.3 # Onsets further apart than this interval will be considered different

NAN_STR = "NAN"
SEP_STR = ",\t" 

def computeDifference(labels_file,extracted_file):
    #print(labels_file.readline())
    #print(extracted_file.readline())
    
    end_flag = False
    lbl_line = labels_file.readline()
    ext_line = extracted_file.readline()
    while not end_flag:
        if lbl_line is "" and ext_line is "": #TODO check closing condition
            end_flag = True
        else:
            lbl_value = float(lbl_line.split()[0] if (lbl_line is not "") else "inf")
            ext_value = float(ext_line.split()[0] if (ext_line is not "") else "inf")
            diff = ext_value - lbl_value + AUBIODELAY_S
                
            if abs(diff) < MAX_ONSET_DIFFERENCE_S:
                print(str(lbl_value) + SEP_STR + str(ext_value) + SEP_STR + str(diff))
                lbl_line = labels_file.readline()
                ext_line = extracted_file.readline()
            elif lbl_value < ext_value:
                print(str(lbl_value) + SEP_STR + NAN_STR + SEP_STR + NAN_STR)
                lbl_line = labels_file.readline()
            elif lbl_value > ext_value:
                print(NAN_STR + SEP_STR + str(ext_value) + SEP_STR + NAN_STR)
                ext_line = extracted_file.readline()
    print("")







onsets_labeled = glob.glob("onsets_labeled/*.txt")

for filename in onsets_labeled:
    filename = os.path.basename(filename)
    file_labels = open("onsets_labeled/"+filename, "r")
    file_extrac = open("onsets_extracted/"+filename, "r")
    computeDifference(file_labels,file_extrac)
    file_labels.close()
    file_extrac.close()


