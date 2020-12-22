# python-rss-scrapper

## Introduction

This project is a simple `RSS scraper` application which saves RSS feeds to a database and lets a user view and manage feeds they’ve added to the system through an API. Think of `Google Feedburner` as an example.

## Tech Stack

- [Docker 19.03.11](<https://www.docker.com/>)
- [docker-compose 1.24.1](<https://docs.docker.com/compose/>)
- [Python 3.8.0](<https://www.python.org/downloads/>)
- [Django 3.1.4](<https://www.djangoproject.com/>)
- [djangorestframework 3.12.2](<https://www.django-rest-framework.org/>)
- [Redis 3.4.1](<https://redis.io/>)
- [Celery 4.4.1](<https://docs.celeryproject.org/en/stable/>)

## Installation and Set Up

1. Execute the command `docker-compose up` inside the `src` folder, after that you just need to wait for the environment sets up
2. Execute the command `make migrate` when docker is already running.
3. You can access the API documentation in <http://localhost:8000/docs/>

## API Utilization

This API uses a `JWT Token` to manage the access to the API, however, to generate this token you first need to create a `superuser` on Django with the command `make createsuperuser`.

After that you need to make a POST request to the endpoint `/api/token/` passing you username and password, example:
```
curl --location --request POST 'http://localhost:8000/api/token/' \
--form 'username="dylan"' \
--form 'password="testing"'
```
This endpoint will generate your JWT key with a `15 minutes` lifetime duration.
```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwODczODQzNSwianRpIjoiMjMyYTg1OGVhMzI1NDU4NWJiNzM1M2Y0N2FmZDFiMTIiLCJ1c2VyX2lkIjoxfQ.Tal2Od253lwiChgxmx5nBa9oTSr-wS1DCWET_5yPP2E",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA4NjUyOTM1LCJqdGkiOiIxZGE3MDJmMjIxM2I0NmMyOTRmMzljZmZhNzI0OThjMiIsInVzZXJfaWQiOjF9.QwczlErSAauzHRs0uZhfyFRlgyYCLyu74vJA4BgoKQA"
}
```

You need to use the `access` one in your header with a prefix `Bearer `, like that:
`--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ...'`

Obs: The `refresh` one is meant to use to refresh your current Token using the endpoint `/api/token/refresh/`, example:
```
curl --location --request POST 'http://localhost:8000/api/token/refresh/' \
--form 'refresh="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwODczODQzNSwianRpIjoiMjMyYTg1OGVhMzI1NDU4NWJiNzM1M2Y0N2FmZDFiMTIiLCJ1c2VyX2lkIjoxfQ.Tal2Od253lwiChgxmx5nBa9oTSr-wS1DCWET_5yPP2E"'
```

## Observation

- You can filter the read/unread items using the endpoint `/feeds/`, you just need to add a querystring, for example:
`http://localhost:8000/items/feed/27a82364-58d9-4cff-abae-14a76ce842e9/?show_all_read=true` or
`http://localhost:8000/items/feed/27a82364-58d9-4cff-abae-14a76ce842e9/?show_all_unread=true` if you want just the `unreads`

I tried to add this on swagger but I couldn't get it, so I decided to not focus on this detail.

## Makefile Commands

- `make makemigrations`: Looks for migrations to create
- `make migrate`: Execute migrations
- `make createsuperuser`: Create a superuser for the application
- `make test`: Execute all tests.

## Tasks

This project has two asynchronous tasks that use Celery and Redis to execute.

- `update_all_feed_items`: This task gets all feed and updates their items, and is executed every 30 minutes automatically.
- `get_items_by_feed`: This task receives a specific feed uuid and updates all his items, and you can call this task using the endpoint `/feeds/{uuid}/update/`.-

Ps: These two tasks have a retry mechanism in case it fails that you can configure using the variables `CELERY_RETRY_DELAY` and `CELERY_MAX_RETRIES` that are in the settings file.

## Author

* **Dylan Martins Janine de Andrade** - [github](https://github.com/dylanmartins) [linkedin](https://www.linkedin.com/in/dylan-m-j-andrade/)
