# My Django-Ninja Project

This is a simple Django-Ninja project demonstrating the use of Django models and Ninja routers to create a RESTful API.

## Project Setup

This project uses pipenv, a packaging tool for Python that solves some common problems associated with the typical workflow using pip, virtualenv, and the good old `requirements.txt`.

### Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of Python and pipenv.
- You have a basic understanding of Python and Django.

### Installing the Project

Install the project dependencies with pipenv:

```bash
pipenv install
```

Create `.env` file based on `.env.example` and fill in your env variables.

### Running the Project

#### Applying Migrations

The `migrate` script applies or unapplies migrations following the order defined in the migration files. This script alters the database schema to match the current state of your models.

```bash
pipenv run migrate
```

#### Importing repeatable job

This project uses `django-rq-scheduler`. A Django extension for RQ (Redis Queue) that provides a database backed job scheduler.

Import job from a JSON file into the RQ Scheduler.

```bash
pipenv run python manage.py import -f json --filename repeatable_job.json
```

#### Running the Worker

The `worker` script starts the RQ (Redis Queue) worker process. This process executes tasks placed on the queue.

```bash
pipenv run worker
```

#### Starting the Server

The `runserver` script starts Django's development server. By default, the server listens on localhost, port 8000.

```bash
pipenv run runserver
```

The server should start on `http://localhost:8000`. You can visit `http://localhost:8000/api/docs` to view the automatically generated API documentation.

## Running Tests

This project uses pytest and pytest-django for testing. To run the tests, use the following command:

```bash
pipenv run test
```
