#!/usr/bin/bash

echo "Provide the name of the asset (directory), not the full path"
/home/so/screening-venv/bin/python /home/so/screening/scripts/elastic.py $1
