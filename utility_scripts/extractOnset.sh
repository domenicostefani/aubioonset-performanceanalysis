#!/bin/bash

# This script simply calls AUBIOONSET with a set of predefined parameters
# It is used to test the accuracy and time delay of the onset detection with
# different methods and initializations
#
# Call this by providing a SINGLE argument: it has to be the audio file in
# analysis.
#
# Author: Domenico Stefani
#          - domenico.stefani[at]unitn.it
#          - domenico.stefani96[at]gmail.com
# Date:   05/11/2020


# +---------------------+
# | Edit these settings |
# +---------------------+

# These are set only if they are not already existent

# Available methods:<default|energy|hfc|complex|phase|specdiff|kl|mkl|specflux>
if [[ -z "$ONSET_METHOD" ]]; then
    echo "using default value for ONSET_METHOD"
    ONSET_METHOD=complex
fi

if [[ -z "$BUFFER_SIZE" ]]; then
    echo "using default value for BUFFER_SIZE"
    BUFFER_SIZE=256
fi
if [[ -z "$HOP_SIZE" ]]; then
    echo "using default value for HOP_SIZE"
    HOP_SIZE=128
fi
if [[ -z "$SILENCE_THRESHOLD" ]]; then
    echo "using default value for SILENCE_THRESHOLD"
    SILENCE_THRESHOLD=-40.0
fi
if [[ -z "$ONSET_THRESHOLD" ]]; then
    echo "using default value for ONSET_THRESHOLD"
    ONSET_THRESHOLD=0.75
fi
if [[ -z "$MINIMUM_INTER_ONSET_INTERVAL_MS_SECONDS" ]]; then
    echo "using default value for MINIMUM_INTER_ONSET_INTERVAL_MS_SECONDS"
    MINIMUM_INTER_ONSET_INTERVAL_MS_SECONDS=0.020 # 20ms
fi



##---- Do not edit what comes after ----##

if [ "$#" -ne 1 ]; then
    echo "ERROR! Usage: extractOnset.sh audioFile.wav"
    exit
fi

fullfilename=$1	      # Use argument as input audio file
filename="${1%.*}"    # Extract filename withoud extension
subdir="onsets_extracted/"
mkdir -p $subdir

# Extract onsets with the parameters chosen
aubioonset $fullfilename -B $BUFFER_SIZE -H $HOP_SIZE -s $SILENCE_THRESHOLD -t $ONSET_THRESHOLD -O $ONSET_METHOD -M $MINIMUM_INTER_ONSET_INTERVAL_MS_SECONDS > $subdir$filename.txt

./utility_scripts/fixLabels.sh $subdir$filename.txt
