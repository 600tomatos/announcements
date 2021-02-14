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

# Deploy stack
$ROOT_ABS_PATH/node_modules/serverless/bin/serverless.js deploy -s ${ENVIRONMENT_NAME}

# Create postman dev environment
_dev_postman_path=$ROOT_ABS_PATH/postman/Announcements-dev.postman_environment.json
_localhost_postman_path=$ROOT_ABS_PATH/postman/Announcements-localhost.postman_environment.json
localhost_url=$(cat $_localhost_postman_path | grep -Poi '"value": "\K(http[s]?:\/\/)?([^\/\s]+\/)([^"]*)')

sed -e 's@'"${localhost_url}"'@'"$(get_current_service_endpoint)"'@g' \
 -e 's@'"Announcements/localhost"'@'"Announcements/dev"'@g'  -- "$_localhost_postman_path" >"$_dev_postman_path"
