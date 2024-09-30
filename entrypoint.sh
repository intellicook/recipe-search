#!/bin/sh

# Run migrations
alembic upgrade head

# Run server
python main.py
