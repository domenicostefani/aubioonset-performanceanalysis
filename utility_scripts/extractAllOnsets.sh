#!/bin/bash

# This script simply calls AUBIOONSET with a set of predefined parameters
# ON ALL THE WAW FILES IN THE CURRENT FOLDER
#
# Author: Domenico Stefani
#          - domenico.stefani[at]unitn.it
#          - domenico.stefani96[at]gmail.com
# Date:   05/11/2020

usage() { echo "Usage: $0 [-B <BUFFER_SIZE>] [-H <HOP_SIZE>] [-s <SILENCE_THRESHOLD>] [-t <ONSET_THRESHOLD> -O <ONSET_METHOD>] [-M <MINIMUM_INTER_ONSET_INTERVAL_SECONDS>]" 1>&2; exit 1; }

while getopts “:B:H:s:t:O:M:” opt; do
  case $opt in
    B) BUFFER_SIZE=$OPTARG ;;
    H) HOP_SIZE=$OPTARG ;;
    s) SILENCE_THRESHOLD=$OPTARG ;;
    t) ONSET_THRESHOLD=$OPTARG ;;
    O) ONSET_METHOD=$OPTARG ;;
    M) MINIMUM_INTER_ONSET_INTERVAL_SECONDS=$OPTARG ;;
    *) usage ;;
  esac
done

echo "BUFFER_SIZE=$BUFFER_SIZE"
echo "HOP_SIZE=$HOP_SIZE"
echo "SILENCE_THRESHOLD=$SILENCE_THRESHOLD"
echo "ONSET_THRESHOLD=$ONSET_THRESHOLD"
echo "ONSET_METHOD=$ONSET_METHOD"
echo "MINIMUM_INTER_ONSET_INTERVAL_SECONDS=$MINIMUM_INTER_ONSET_INTERVAL_SECONDS"


# Available methods:<default|energy|hfc|complex|phase|specdiff|kl|mkl|specflux>
if [[ -z "$ONSET_METHOD" ]]; then
    echo "using default value for ONSET_METHOD"
    ONSET_METHOD=default
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
if [[ -z "$MINIMUM_INTER_ONSET_INTERVAL_SECONDS" ]]; then
    echo "using default value for MINIMUM_INTER_ONSET_INTERVAL_MS_SECONDS"
    MINIMUM_INTER_ONSET_INTERVAL_SECONDS=0.020 # 20ms
fi


# Call extractOnset for all waw files in the folder
for audiofile in *.wav; do
	source ./utility_scripts/extractOnset.sh $audiofile
done

DELAY=$(python -c "print(int($HOP_SIZE*4.3))")

if [[ $ONSET_METHOD = "complex" ]] ; then
	DELAY=$(python -c "print(int($HOP_SIZE*4.6))")
fi

echo "To get the real detection time, add the delay of $DELAY samples"
