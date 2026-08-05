#!/bin/bash
set -e
cd /home/firebot/git/meow-bot
git fetch
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse @{u})
if [ "$LOCAL" != "$REMOTE" ]; then
    git pull
    pkill -f "python3 bot.py" || true
    nohup python3 bot.py > bot_runtime.log 2>&1 &
fi
