#!/usr/bin/env bash
set -e

supervisord -n -c /etc/supervisor/app.conf
