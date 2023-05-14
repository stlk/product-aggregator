ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel

RUN mkdir -p /app
WORKDIR /app

COPY Pipfile Pipfile.lock .
RUN pip install pipenv --upgrade --upgrade-strategy only-if-needed
RUN pipenv install --system --skip-lock

COPY . .

ENV API_BASE_URL=placeholder
ENV API_REFRESH_TOKEN=placeholder
RUN python manage.py collectstatic --noinput


EXPOSE 8080

CMD ["waitress-serve", "--port", "8080", "product_aggregator.wsgi:application"]
