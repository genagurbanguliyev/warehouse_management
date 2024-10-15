# This is WhereHouse Management system
Written in:
 - API - FastAPI
 - tests - pytest
***
## Installation
**Used:**
 - Python (version 3.11.5)
 - Poetry (version 1.8.3)
***
Step 1: \
Install `poetry` to your system (here official [site](https://python-poetry.org/docs/#installing-with-pipx) )

Step 2:
Go to root directory of project.
 - Run: `poetry shell` - to activate the virtual env
 - Run `poetry install` to install dependencies

Step 3:\
If you want to take advantage of `Taskfile` to install it to your system: \
(if your system is Linux then run just this command: `sudo snap install task --classic`)
or here is official [site](https://taskfile.dev/installation/)\
After installing `Taskfile` you can run `task -l` to list all tasks.


***
## Testing
for testing app:
FIRST set `.env` file `ENVIRONMENT=test` \
Run: `pytest` in root directory of project

***
## Up in docker:
```bash
docker compose up
```