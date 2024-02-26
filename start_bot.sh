#!/bin/bash
# Script to start in a while the discord_bot with bot.py main file.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR" || exit

while true; do
    sudo python3 bot.py
done
