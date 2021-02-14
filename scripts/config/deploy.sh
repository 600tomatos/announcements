#!/usr/bin/env bash
ROOT_ABS_PATH="$(cd "$(dirname $(dirname $(dirname "${BASH_SOURCE[0]}")))" >/dev/null && pwd)"

source $ROOT_ABS_PATH/scripts/config/common.sh
source $ROOT_ABS_PATH/scripts/config/environments.sh

declare_deploy_envs

if [ -z $PIPENV_ACTIVE ]; then
  cd $ROOT_ABS_PATH
  colored $RED 'entering to pipenv shell.. Run command again\n'
  pipenv shell
fi

function check_user_agreement() {
  while true; do
    read -p "Do you want to continue?" yn
    case $yn in
    [Yy]*) break ;;
    [Nn]*) exit ;;
    *) echo "Please answer yes or no." ;;
    esac
  done
}

user_input_environment 'Enter a number that matches the name of the environment you want to upgrade'

check_user_agreement

$ROOT_ABS_PATH/node_modules/serverless/bin/serverless.js deploy -s ${ENVIRONMENT_NAME}
