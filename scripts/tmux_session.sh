#!/usr/bin/env bash

# Create a tmux session and run command(s).

session="shea"
directory="$HOME/shea"

if /usr/bin/tmux has-session -t $session > /dev/null 2>&1; then
  echo "[ FAIL ] Session $session already running!"
  exit 1
else
  echo "[ INFO ] Starting $session."
  /usr/bin/tmux new-session -d -s $session
  /usr/bin/tmux send-keys -t $session "cd $directory" C-m
  /usr/bin/tmux send-keys -t $session "make run" C-m
  if [ $? -eq 0 ]; then
    echo "[  OK  ] $session started successfully."
  else
    echo "[ FAIL ] $session failed to start!"
  fi
fi
