#!/usr/bin/env bash

if [ -n "$1" ]; then
    export PORT=$1
else
    export PORT=5000
fi

[ -d "venv" ] && . venv/bin/activate

gunicorn eHoshin.wsgi -b 0.0.0.0:$PORT --reload --error-logfile "-" --enable-stdio-inheritance --log-level "debug"
