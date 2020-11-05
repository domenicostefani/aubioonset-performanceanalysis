#!/bin/bash

mkdir -p toremove

for file in *.txt; do
    mv --backup=numbered $file toremove/
done
