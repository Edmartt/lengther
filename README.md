# Locstorager

locstorager is a microservice that has endpoints to store locations with name, latitude and longitude in a SQL database. The purpose is to store these locations so that later the wrapper-piper service with two ids can make a distance calculation using the Euclidean formula.

For every location saved, we need to return the location id property


## Requirements

- Python 3.11
- Docker
- Postgres

## Project structure

```
.
├── config.py
├── Dockerfile
├── envrc.example
├── README.md
├── requirements.txt
├── run.py
└── src
    ├── database
    │   ├── db_interface.py
    │   ├── __init__.py
    │   ├── postgres.py
    │   └── schema.py
    ├── __init__.py
    └── locations
        ├── cache
        │   ├── cache_redis.py
        │   └── __init__.py
        ├── data
        │   ├── __init__.py
        │   ├── pg_access_interface.py
        │   └── pg_data_access.py
        ├── hooks.py
        ├── __init__.py
        ├── locs.py
        ├── models
        │   ├── __init__.py
        │   └── model.py
        └── routes.py
```

## Running

1. Clone the repo

```
https://github.com/Edmartt/locstorager.git
```

2. Browse into the project folder

```
cd locstorager/
```

## Running with Flask

1. Create virtual environment

```
python3 -m venv <virtual environment name>
```


2. Activate virtual environment

```
source env/bin/activate
```

3. Install dependencies

```
pip3 install -r requirements
```

4. set the environment variables following the envrc.example

```
source .envrc
```

5. Run

```
flask run -p <port>
```

## Running with Docker

1. Pull the image from Dockerhub

```
docker pull edmartt/locstorager
```

2. set .env file following env.example

3. Create container

```
docker run --rm -p <host-port:docker-port> --env-file .env edmartt/locstorager
```

### Note

This service requires a postgres database, and a redis instance running, so, if we send some requests for saving data in the database we'll get an error. If we try to get all the locations we'll see an erro related to REDIS, this is normal because this service is intended to be attached with docker compose in this project [wrapper-piper](https://github.com/Edmartt/wrapper-piper). You'll find the endpoint docs and the deployment with docker compose in that repo.
