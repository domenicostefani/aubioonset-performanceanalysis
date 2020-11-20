#!/bin/bash

COUNTER=1
while read p; do   echo -e "$p\t$p\t$COUNTER";((COUNTER++)); done <$1 > temp-fixlabels.txt

mv temp-fixlabels.txt $1	
