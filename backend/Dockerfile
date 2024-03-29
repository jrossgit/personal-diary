### Base Python install image
FROM ubuntu:focal AS base

# Install dependencies
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
    python3-pip python3-dev python3-setuptools libpq-dev postgresql-client-12 python3-venv build-essential curl

RUN pip3 install --upgrade pip

# Set python aliases for python3
RUN ln -s /usr/bin/python3 /usr/bin/python

### Poetry installation and setup
FROM base as requirements

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.3.2
ENV PATH="/root/.local/bin:/usr/bin:$PATH"

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --without-hashes -o requirements.txt


### Main installation
FROM base AS build

COPY . /app
WORKDIR /app

# Install Python dependencies
COPY --from=requirements requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000
CMD 'bash -c "python manage.py migrate && python manage.py collectstatic && python manage.py runserver 0.0.0.0:8000'
