#!/bin/bash

# Change directory to be where the command is.
cd "$(cd "$(dirname "$0")" > /dev/null && pwd)"

# Print the working directory for example.
pwd

# Run nodemon
python3 -u index.py