#!/bin/bash
clear

source /fastapi_app/docker/seeders.sh

gunicorn app.main:app -w 2 -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
