#!/usr/bin/env bash
ROOT_ABS_PATH="$(cd "$(dirname $(dirname $(dirname "${BASH_SOURCE[0]}")))" >/dev/null && pwd)"

source $ROOT_ABS_PATH/scripts/config/common.sh

if [ -z $PIPENV_ACTIVE ]; then
  cd $ROOT_ABS_PATH
  colored $RED 'entering to pipenv shell.. Run command again\n'
  pipenv shell
fi

if [ ! -d "$ROOT_ABS_PATH/node_modules" ]; then
  colored $RED "It seems that you have not activated the virtual environment. Run the 'make init' command first\n"
else
  sls dynamodb start &
  P1=$!
  $ROOT_ABS_PATH/node_modules/serverless/bin/serverless.js wsgi serve  &
  P2=$!
  wait $P1 $P2
fi
