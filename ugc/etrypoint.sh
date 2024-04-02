#!/bin/sh

cd src || exit

gunicorn --worker-class gevent --workers 4 --bind "0.0.0.0:5001" --log-level debug main:app
