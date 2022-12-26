#!/usr/bin/bash

BASE=/home/so/chainsaw
BASE_OUTPUT=/home/so/screening/output/
CHAINSAW=$BASE/chainsaw_x86_64-unknown-linux-mus 
SIGMA=$BASE/sigma/
RULES=$BASE/rules/
#MAPPINGS=$BASE/mappings/sigma-event-logs-all.yml
MAPPINGS=$BASE/mappings/cudeso.yml

JSON_OUT=`echo $1 | cut -d '/' -f 6`

$CHAINSAW hunt -s $SIGMA --mapping $MAPPINGS -r $RULES  --csv --output $BASE_OUTPUT/${JSON_OUT}-chainsaw $1 
