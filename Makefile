# Lithium Django Project Makefile
# Helper commands for development workflow

.PHONY: build up down restart logs shell django-shell test migrate makemigrations collectstatic createsuperuser help

# Default target
.DEFAULT_GOAL := help

# Variables
DOCKER_COMPOSE = docker-compose
DOCKER_EXEC = $(DOCKER_COMPOSE) exec web
MANAGE_PY = python manage.py

# Docker commands
build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up

up-d:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

restart:
	$(DOCKER_COMPOSE) restart

logs:
	$(DOCKER_COMPOSE) logs -f

# Django commands
shell:
	$(DOCKER_EXEC) bash

django-shell:
	$(DOCKER_EXEC) $(MANAGE_PY) shell

test:
	$(DOCKER_EXEC) $(MANAGE_PY) test

migrate:
	$(DOCKER_EXEC) $(MANAGE_PY) migrate

makemigrations:
	$(DOCKER_EXEC) $(MANAGE_PY) makemigrations

collectstatic:
	$(DOCKER_EXEC) $(MANAGE_PY) collectstatic --noinput

createsuperuser:
	$(DOCKER_EXEC) $(MANAGE_PY) createsuperuser

# Help command
help:
	@echo "Available commands:"
	@echo "  build          - Build Docker images"
	@echo "  up             - Start containers in foreground"
	@echo "  up-d           - Start containers in background"
	@echo "  down           - Stop and remove containers"
	@echo "  restart        - Restart containers"
	@echo "  logs           - View container logs"
	@echo "  shell          - Open a bash shell in the web container"
	@echo "  django-shell   - Open Django shell in the web container"
	@echo "  test           - Run Django tests"
	@echo "  migrate        - Apply database migrations"
	@echo "  makemigrations - Create new database migrations"
	@echo "  collectstatic  - Collect static files"
	@echo "  createsuperuser - Create a Django superuser"
