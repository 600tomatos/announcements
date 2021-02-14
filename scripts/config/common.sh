#!/bin/bash

RED='\033[1;31m'
BLUE='\033[1;34m'
GREEN='\033[1;32m'
NC='\033[0m'

ENVIRONMENT_NAME=""
_ANY=""

function colored() {
  printf "$1$2${NC}"
}

unameOut="$(uname -s)"
case "${unameOut}" in
Linux*) machine=Linux ;;
Darwin*) machine=Mac ;;
esac

function show_numered_items() {
  counter=0
  for i in "$@"; do
    ((counter++))
    printf "%s  %s\n" $(colored $BLUE "[$counter]") $i
  done
}

function user_input_environment() {
  printf '\n\n'
  colored $BLUE "$1: \n\n"
  names=("${!environment@}")
  counter=0
  declare -n arr_ref
  for arr_ref in "${names[@]}"; do
    ((counter++))
    arr_ref["counter"]+="$counter"
    printf "%s  %s\n" $(colored $BLUE "[$counter]") "${arr_ref[name]}"
  done
  printf '\n'
  while [[ -z "$ENVIRONMENT_NAME" ]]; do
    read -r -p ">>> " VAL
    if [[ -z "$VAL" ]]; then
      colored $RED '\ninvalid input, try again...\n'
    else
      declare -n arr_ref
      for arr_ref in "${names[@]}"; do
        if [ "${arr_ref[counter]}" = "$VAL" ]; then
          ENVIRONMENT_NAME="${arr_ref[name]}"
          printf '\n'
          break
        fi
      done
      if [ -z "$ENVIRONMENT_NAME" ]; then
        counter=0
        colored $RED "invalid input  '${VAL}'\n"
        printf "available numbers: \n\n"
        for arr_ref in "${names[@]}"; do
          ((counter++))
          printf "%s  %s\n" $(colored $BLUE "[$counter]") "${arr_ref[name]}"
        done
        printf '\n'
        continue
      else
        break
      fi
    fi
  done
}

function user_input_any() {
  printf '\n\n'
  colored $GREEN "$1: \n\n"
  [ -z "$2" ] && invitation=">>> " || invitation=">>> [$2] "
  read -r -p "${invitation}" VAL
  _ANY=${VAL:-$2}
}

function command_exists() {
  command -v "$@" >/dev/null 2>&1
}

function get_current_stage_key() {
  _bgv=$(aws cloudformation --region us-east-2 describe-stacks --stack-name "rise-api-blue-green-${ENVIRONMENT_NAME}" --query "Stacks[0].Outputs[?OutputKey=='CurrentGreenKey'].OutputValue" --output text)
  echo $_bgv
}
