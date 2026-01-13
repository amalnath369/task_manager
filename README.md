# Task Management Application

## Overview

Task management system with role-based access, task completion reports, and custom admin panel built using Django and Django REST Framework.

# Features

## Authentication & Authorization

JWT authentication, role-based access (SuperAdmin, Admin, User), web and API login/logout.

## Task Management

CRUD tasks, status workflow, completion reports, worked hours, due dates.

## Role-Based Access

SuperAdmin, Admin, and User permissions enforced across web and API.

## Reporting

Task completion reports and worked-hours tracking.

# Technology Stack

## Backend

Django 4.2.7, Django REST Framework 3.14.0

## Database

SQLite (3NF compliant)

## Authentication

JWT (Simple JWT)

## Frontend

HTML, Bootstrap 5

## Deployment

Docker, Docker Compose, Gunicorn, WhiteNoise

# Database Design

## Users

id, username, email, role, admin_id, audit fields

## Tasks

id, title, description, assigned_to, assigned_by, due_date, status, completion_report, worked_hours, completed_at

# API Endpoints

## User APIs

POST /users/api-login/
POST /users/api-logout/
GET /users/
POST /users/
GET /users/<id>/
PUT /users/<id>/
GET /users/admins/

## Task APIs

GET /tasks/api-task
POST /tasks/api-task
GET /tasks/api-task/<id>/
PUT /tasks/api-task/<id>/
GET /tasks/<id>/report/

# Web URLs

## Authentication

/users/login/
/users/logout/

## Dashboards

/tasks/
/tasks/dashboard/

## Management

/tasks/users/
/tasks/admins/

# URL Configuration

## Users App

/login/
/logout/
/
/<id>/
/admins/
/api-login/
/api-logout/

## Tasks App

/dashboard/
/
/<task_id>/
/users/
/admins/
/api-task
/api-task/<id>/
/<id>/report/

# Swagger Documentation

## Swagger UI

/swagger/

## Redoc

/redoc/

# Installation

## Docker

Clone repository and run docker-compose up --build

## Local

Create venv, install requirements, migrate, runserver

# Testing

## Django Tests

python manage.py test

# Environment Variables

## Required

SECRET_KEY, DEBUG, ALLOWED_HOSTS, DATABASE_URL

# License

MIT
