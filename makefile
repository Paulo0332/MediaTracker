# ================================================================
# 🧰 Makefile — MediaTracker Project
# Simplifies running Docker Compose and Django commands.
# ================================================================

SERVICE_NAME = web

# ------------------------------------------------
# 🏗️ INFRASTRUCTURE MANAGEMENT
# ------------------------------------------------

# Start all services in detached mode
up:
	docker compose up -d

# Build images (first-time setup or after Dockerfile changes)
up-build:
	docker compose up --build -d

# Stop and remove containers/networks
down:
	docker compose down

# Full clean — removes containers, networks, images, and volumes
# ⚠️ WARNING: Deletes database data (postgres_data)!
clean:
	docker compose down -v --rmi all

# ------------------------------------------------
# ⚙️ DJANGO APPLICATION COMMANDS
# ------------------------------------------------

# Run database migrations
migrate:
	docker compose exec $(SERVICE_NAME) python manage.py migrate

# Create a Django superuser (interactive)
superuser:
	docker compose exec $(SERVICE_NAME) python manage.py createsuperuser

# Run Django’s development server
runserver:
	docker compose exec $(SERVICE_NAME) python manage.py runserver 0.0.0.0:8000

# Open a shell inside the web container
sh:
	docker compose exec $(SERVICE_NAME) /bin/bash

# Tail logs from the web service
logs:
	docker compose logs -f $(SERVICE_NAME)

# Run test suite
test:
	docker compose exec $(SERVICE_NAME) python manage.py test
