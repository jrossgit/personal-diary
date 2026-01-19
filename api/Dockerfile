# Borrowed from https://github.com/orgs/python-poetry/discussions/1879

### Base Python install image
FROM python:3.14-slim-bookworm as python-poetry-build-base

# python no pyc files + pip longer timeout
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry set location
    POETRY_VERSION=2.2.1 \
    POETRY_HOME="/opt/poetry" \
    \
    # Poetry can create a venv for you, but it will be a random venv name 
    # You could also have POETRY_VIRTUALENVS_IN_PROJECT=1 to get a deterministic venv name
    # but it will be in the project directory, which might cause problem if you wanna mount your project in dev
    # Instead we create/activate our own venv in a known location, prompting poetry to use it
    # Once poetry lets us set the venv name in its confing, we can remove this 
    # Ref: https://github.com/python-poetry/poetry/issues/263#issuecomment-1404129650
    VIRTUAL_ENV="/opt/pysetup/venv"

# create the venv and activate it
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install poetry 
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential
# use official curl to respect $POETRY_VERSION & $POETRY_HOME
# (pip install poetry doesn't respect $POETRY_HOME)
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

# builder-base installs shared deps (dev + prod), but not the root package.
# We skip root package here to control how/when it's installed later (editable vs wheel),
# and to avoid copying source code into this stage.
FROM python-poetry-build-base AS builder-base

# install the common deps, filter the group you want
COPY poetry.lock pyproject.toml ./
RUN poetry install --without dev --no-root


# `development` image is used during development
FROM python-poetry-build-base AS development

# copy in our poetry and base built venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $VIRTUAL_ENV $VIRTUAL_ENV
WORKDIR /app
# copy image-specific deps, filter the group you want
COPY --from=builder-base poetry.lock pyproject.toml ./
RUN poetry install --only dev --no-root
# Install root package in editable mode (default for Poetry)
# Dummy README to satisfy Poetry≈
# Use touch to avoid cache busting on real README changes
RUN touch README.md
COPY . .
CMD alembic -x url=${SQL_DATABASE} upgrade head && fastapi dev diary_api/main.py --host 0.0.0.0 --port 8000

# # Set python aliases for python3
# RUN ln -s /usr/bin/python3 /usr/bin/python

# RUN pipx install poetry==2.2.1
# ENV PATH="/root/.local/bin:/usr/bin:$PATH"

# COPY . /app
# WORKDIR /app

# # # Install Python dependencies
# RUN poetry install

# # # TODO: Run via uwsgi
# EXPOSE 8000
# CMD ["alembic", "upgrade", "head", "&&", "fastapi", "run", "app/main.py", "--port", "80"]
