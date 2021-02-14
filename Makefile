SHELL := /usr/bin/env bash

init:
	@scripts/config/configure/init.sh

run:
	@scripts/config/run.sh || true

deploy:
	@scripts/config/deploy.sh || true
