#!/bin/bash
#    File: run.sh
#    Creator: Ernest M Duckworth IV
#    Created: Monday Feb 21 2022 at 11:49:08 AM
#    For: 
#    Description:
#Colors
NO='\033[0m'
R='\033[0;31m'
G='\033[0;32m'
O='\033[0;33m'

PROGRAM="/Users/rionduckworth/codeProjects/school/cs370/src/main.py"

function main() {
   echoColor $G "Starting Bot"
   python3 "$PROGRAM"
   if [[ $? -eq 0 ]]
   then
      local status=$G
   else
      local status=$R
   fi
   echoColor $status "Ending Bot"
}

function echoColor() {
   echo -e "${1}$2${NO}"
}

function echoErr() {
   echoC $R $1
}

main
