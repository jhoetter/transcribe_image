#!/bin/sh
set -e

# Install adalace package in development mode
pip install -e /app/adalace-engine

# Execute the command
exec "$@"