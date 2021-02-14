#!/usr/bin/env bash

ROOT_ABS_PATH="$( cd "$(dirname $(dirname $(dirname $( dirname "${BASH_SOURCE[0]}" ))))" >/dev/null && pwd )"


source $ROOT_ABS_PATH/scripts/config/common.sh
colored $BLUE "\nThe application is running on ${machine} operation system...\n"

sls_exe=$ROOT_ABS_PATH/node_modules/serverless/bin/serverless.js

PYTHON_EXECUTOR=''

_python_ex=$(python3.7 --version)
_python3_ex=$(python3 --version)

read -d '' waring <<EOF
Seems you do not have python3.7 installed or I cannot find python executor by alias "python3.7".
This project requires python3.7 to be in your system path. Install python3.7
or create an alias named python3.7. You can see if python3.7 is installed by running "python3.7 -V"
EOF

if [[ $_python_ex == *"3.7"* ]]; then
  PYTHON_EXECUTOR=$(which python3.7)
elif [[  $_python3_ex == *"3.7"* ]]; then
 PYTHON_EXECUTOR=$(which python3)
fi

if [[ -f "$PYTHON_EXECUTOR" ]]; then
   colored $GREEN "Python executor path = ${PYTHON_EXECUTOR}\n"
else
  colored $RED "$waring\n\n"
fi

if [ $machine == 'Linux' ]; then
  printf 'npm version:  '
  npm -v  ||  (cd /tmp && curl -L https://npmjs.org/install.sh | sudo sh) && cd $ROOT_ABS_PATH
  node_major_ver=$(node -v | sed 's/.v*\([0-9]*\).*/\1/')
  if [ -z $node_major_ver ]; then
     colored $BLUE 'install node js'
    sudo apt-get install nodejs
  fi
  if (( $node_major_ver < 10 )); then
     colored $BLUE 'update node js'
    sudo npm install -g n
    sudo n latest
  fi


elif [ $machine == 'Mac' ]; then
  printf 'npm version:  '
  npm -v  || brew install node
  [[ $BASH_VERSION = 3.*  ]] && ((brew unlink bash || true) && brew update && brew install bash)
fi

if [ ! -d "$ROOT_ABS_PATH/node_modules" ]; then
    colored $BLUE 'install node dependencies...'
    (npm i || sudo npm i) && cd $ROOT_ABS_PATH
fi

# Install dynamo db locally
$sls_exe dynamodb install

$PYTHON_EXECUTOR -m pip install pipenv
$PYTHON_EXECUTOR -m pipenv install --dev --python=$PYTHON_EXECUTOR
$PYTHON_EXECUTOR -m pipenv shell

