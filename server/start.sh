#!/bin/sh

python3 SqliteClasses.py sql_scripts/DatabaseCreate.sql # INITIALIZING SQLITE DATABASE
uvicorn main:app # RUNNING SERVER