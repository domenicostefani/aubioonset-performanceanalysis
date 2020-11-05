#!/bin/bash

# This script simply calls AUBIOONSET with a set of predefined parameters
# ON ALL THE WAW FILES IN THE CURRENT FOLDER
#
# Author: Domenico Stefani
#          - domenico.stefani[at]unitn.it
#          - domenico.stefani96[at]gmail.com
# Date:   05/11/2020

# +---------------------+
# | Edit these settings |
# +---------------------+

# Available methods:<default|energy|hfc|complex|phase|specdiff|kl|mkl|specflux>
ONSET_METHOD="default"
BUFFER_SIZE=256
HOP_SIZE=64
SILENCE_THRESHOLD=-38.0
ONSET_THRESHOLD=0.
MINIMUM_INTER_ONSET_INTERVAL_MS_SECONDS=0.020 # 20ms

# Call extractOnset for all waw files in the folder
for audiofile in *.wav; do
	source ./utility_scripts/extractOnset.sh $audiofile
done

DELAY=$(python -c "print(int($HOP_SIZE*4.3))")

if [[ $ONSET_METHOD = "complex" ]] ; then
	DELAY=$(python -c "print(int($HOP_SIZE*4.6))")
fi

echo "To get the real detection time, add the delay of $DELAY samples"
