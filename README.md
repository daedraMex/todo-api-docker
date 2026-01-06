# TODO Backend  

author : Erika F.

status : in-progress

last update: 06- jan- 2026
<hr/>

## Tech

- Python 3.11
- FastAPI
- Docker
- PostgreSQL

## Docs

## System Requirements

- [git](git) v2.13 or greater

## Branches

- main: production code
- dev: development code

## 🚀 Getting Started

1. Environment Configuration
To connect the application to your database and enable security features, you must configure your environment variables.
Create a `.env` file in the root directory of your project and add the values variables:

```bash
cp .env-example .env
```

Then, open the `.env` file and set the appropriate values for each variable according to your setup.

| Variable | Description | Example Value |
|----------|-------------|----------------|
| DB_USER | Your database username | postgres |
| DB_PASSWORD | Your database password | your_password |
| DB_NAME | The name of the project database | task_db |
| DJANGO_SECRET_KEY | Secret key for session tokens | long_random_string |
| PORT | Local server port | 3000 |

1. If is your first tme running the app

```bash
docker compose up --build -d
```

2.For subsequent runs, build the Docker images

```bash
docker compose up -d
```

You can then visit <http://localhost:8000> to see your FastAPI welcome message.

## Goals
