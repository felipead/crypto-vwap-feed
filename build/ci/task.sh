#!/usr/bin/env bash
set -e

task=${1:-'test'}
echo "Running CI task: '${task}'"

cd /home/app

case ${task} in
test)
  pytest "${*:2}"
  ;;
*)
  echo "ERROR: invalid container runtime task: '${task}'"
  exit 1
  ;;
esac
