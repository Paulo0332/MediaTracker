# MediaTracker

> **Work in progress** — a Django application for organizing movies, TV series, games, books, anime, and other media in one personal library.

MediaTracker is being developed as a personal media-tracking hub. The goal is to let users discover titles through external APIs, save them to a collection, follow their progress, and write ratings and reviews. The repository currently contains the data models, initial server-rendered pages, user authentication, and the beginnings of the TMDB integration. **Not all planned features are available through the UI yet.**

## Contents

- [Current status](#current-status)
- [Features and roadmap](#features-and-roadmap)
- [Technology stack](#technology-stack)
- [Architecture](#architecture)
- [Project structure](#project-structure)
- [Local development](#local-development)
- [Running tests](#running-tests)
- [Known limitations](#known-limitations)

## Current status

| Area | Status | Details |
| --- | --- | --- |
| Django project and PostgreSQL | Implemented | Configured with Docker Compose |
| User accounts | Partially implemented | Custom user model, login/logout views, admin integration; no public signup flow yet |
| Media catalog | Implemented (basic) | Authenticated list view and detail view for records already in the database |
| Personal tracking | Data model implemented | Per-user status, rating and review, including uniqueness and validation rules |
| TMDB integration | In progress | HTTP client, movie/series search and detail methods, and DTO mapping |
| Importing external results into the catalog | In progress | Ingestion service exists but is not yet integrated into the UI |
| Games, books, anime and album API integrations | Planned | Model categories exist; provider integrations are not complete |
| Search, favorites, progress and review UI | Planned | Not yet available as a complete end-to-end user workflow |

## Features and roadmap

**Already in the codebase**

- Custom Django user model with unique email addresses.
- Login and logout pages, plus Django admin management.
- Media model supporting movies, series, anime, books, albums and games.
- Catalog listing (`/media/`) and media detail pages (`/media/<id>/`).
- User-to-media collection model with statuses: *Plan to Start*, *In Progress*, *Completed*, *On Hold* and *Dropped*.
- Rating range from 1 to 10 and a rule preventing ratings or reviews for items still marked *Plan to Start* (enforced through Django model validation).
- TMDB movie and TV-series clients for search and details, with provider-response mapping into a normalized immutable DTO.
- Unit tests for DTO parsing, HTTP client behavior and collection-model constraints.

**Still being developed**

- Connect external search results to the user-facing interface.
- Complete media ingestion and persistence integration.
- Add collection management, progress tracking, ratings and reviews through the UI.
- Integrate data providers for additional media types.
- Extend testing and polish the user experience.

## Technology stack

| Layer | Technologies |
| --- | --- |
| Language | Python 3.12 |
| Backend | Django 5 |
| Database | PostgreSQL 15 |
| HTTP integrations | HTTPX; TMDB API |
| UI | Django templates, Bootstrap 5, CSS |
| API dependencies | Django REST Framework and Simple JWT installed (API endpoints not yet exposed) |
| Development environment | Docker, Docker Compose, VS Code Dev Containers |
| Testing | Django test runner, `unittest.mock` |

## Architecture

The project separates application data, per-user tracking and external service integration:

- **`accounts`** — custom users, authentication views/forms and admin customization.
- **`media`** — shared media records, catalog views and templates.
- **`user_media`** — each user's relationship to media, with status, rating and review.
- **`services/api_clients`** — reusable HTTP transport and TMDB-specific API requests. The base client normalizes requests and wraps timeout, transport and HTTP-status errors.
- **`services/dtos.py`** — immutable `MediaItemDTO` and explicit TMDB movie/series payload mapping.
- **`services/media_service.py`** — an ingestion service intended to translate DTOs into persisted `Media` records.

The integration layer isolates TMDB's payload format from the application's internal representation. This is an architectural foundation in progress, not a claim that every integration workflow is already complete.

## Project structure

```text
MediaTracker/
├── .devcontainer/
│   └── devcontainer.json
├── backend/
│   ├── accounts/           # User model, forms, login and admin
│   ├── core/               # Django settings and root URL configuration
│   ├── media/              # Catalog model, views, templates and admin
│   ├── services/
│   │   ├── api_clients/    # Base HTTP client and TMDB client
│   │   ├── tests/          # Service and DTO tests
│   │   ├── dtos.py
│   │   └── media_service.py
│   ├── static/             # Shared styles
│   ├── templates/          # Base template and navbar
│   ├── user_media/         # Personal collection model and tests
│   └── manage.py
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── makefile
├── requirements.txt
└── wait_for_db.sh
```

## Local development

### Prerequisites

- Git
- Docker Engine/Desktop with the Docker Compose plugin
- Optional: VS Code with the Dev Containers extension

### 1. Clone the repository

```bash
git clone https://github.com/Paulo0332/MediaTracker.git
cd MediaTracker
```

> **Branch note:** The work described here is on `feat/api-integration`, and may not yet be present on the default `master` branch. To inspect this development snapshot, run `git switch feat/api-integration`.

### 2. Configure environment variables

Create a `.env` file in the repository root. The current `.env.example` requires cleanup before being used directly: it contains decorative text, and its `MOVIE_API_KEY` name does **not** match the `TMDB_API_TOKEN` read by Django. Use the following minimal example instead:

```dotenv
POSTGRES_DB=mediatracker
POSTGRES_USER=mediatracker
POSTGRES_PASSWORD=replace_with_a_local_password

SECRET_KEY=replace_with_a_long_random_django_secret_key
DEBUG=True
DB_HOST=db
DB_PORT=5432
TMDB_API_TOKEN=
```

Generate a secret key locally, for example:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copy the generated value into `SECRET_KEY`. Obtain a TMDB API read-access token if you intend to use the TMDB client; leave `TMDB_API_TOKEN` empty only when working on functionality that does not require it. **Never commit your real `.env` file or credentials.**

### 3. Start the containers

From the repository root:

```bash
docker compose up --build -d
docker compose exec web python manage.py migrate
```

The Compose configuration starts Django on **http://localhost:8000** and a PostgreSQL container. The `web` service waits for the database port before launching the development server.

To create an admin account:

```bash
docker compose exec web python manage.py createsuperuser
```

Visit:

- `http://localhost:8000/accounts/login/` — login
- `http://localhost:8000/media/` — catalog (login required)
- `http://localhost:8000/admin/` — Django admin

The catalog may initially be empty. Use the admin interface to manage records while the public creation/import workflow is being developed. The root URL (`/`) is not currently configured as a landing page.

### Alternative: VS Code Dev Container

Open the repository in VS Code with the **Dev Containers** extension and select **Reopen in Container**. The configuration attaches to the Compose `web` service. Set up `.env` first, and run the migrations as shown above.

### Useful commands

```bash
docker compose up -d
docker compose logs -f web
docker compose exec web python manage.py migrate
docker compose exec web python manage.py test
docker compose down
```

The repository also includes a `makefile` with targets such as `up`, `up-build`, `migrate`, `superuser`, `test` and `down`. **Caution:** `make clean` removes Docker volumes, including the local PostgreSQL data volume.

## Running tests

With the containers running and the database configured:

```bash
docker compose exec web python manage.py test
```

For a focused test module:

```bash
docker compose exec web python manage.py test services.tests.test_dtos
```

The current repository contains tests for media DTO transformations, base HTTP client behavior and user-media model rules. Some service test modules are still placeholders. These are unit/model tests and do not establish that the entire end-to-end application is production-ready.

Built as an ongoing software-engineering project. Contributions and improvements can be tracked through the repository history.
