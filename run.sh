#!/bin/bash

LOCKFILE=/tmp/puregym.lock
WORKDIR="YOUR SCRAPER.PY FILE LOCATION"
OUTPUT="YOUR OUTPUT FILELOCATION"

cd "$WORKDIR"

if [ ! -e "$LOCKFILE" ]; then
    touch "$LOCKFILE"
    source venv/bin/activate
    START_TIME=$(date +%s)
    ATTENDANCE=$(python scraper.py <username> <email> | head -n 1)
    RESULT=$?
    END_TIME=$(date +%s)
    ELAPSED_TIME=$((END_TIME - START_TIME))
    deactivate
    if [ $RESULT -eq 0 ]; then
        TIMESTAMP=$(date +'%Y-%m-%d %H:%M:%S')
        echo "$TIMESTAMP,$ATTENDANCE,$ELAPSED_TIME" >> output.csv
        tail -n 1 output.csv >> "$OUTPUT"
    else
        echo "Script failed with exit code $RESULT."
    fi
    rm "$LOCKFILE"
else
    echo "Script is already running."
fi
