swagger link:
http://127.0.0.1:8000/swagger/


Budget Project - Personal Budget Management REST API

A Django REST Framework backend application for personal budget tracking and expense management. It allows users to register, log their daily expenses, create monthly budget plans, and receive real-time feedback on whether they are staying within their financial targets.

Core Features

User Management - Custom user model with UUID primary keys, registration, and JWT-based authentication (via Djoser + SimpleJWT).

Expense Tracking - Users can create, read, update, and delete expenses categorized by type (e.g. food, transport). Expenses are filterable by year, month, day, and hour.

Budget Plans - Users can set monthly budget plans with an overall spending target and a target date.

Plan Items - Each plan can be broken down into per-category budget allocations (nested under plans via drf-nested-routers).

Budget Monitoring - The API calculates daily and monthly spending totals and compares them against the user's active plan, returning warnings when a target is exceeded or encouragement when spending is on track.

Per-Category Monitoring - A dedicated endpoint checks whether spending in a specific category has exceeded the allocated plan item amount.

API Documentation - Auto-generated Swagger and ReDoc documentation via drf-yasg.



Tech Stack

Layer     	Technology
Framework	   Django 5.2
API	Django   REST Framework 3.16
Auth	       JWT (SimpleJWT + Djoser)
Routing	     drf-nested-routers
Docs	       drf-yasg (Swagger / ReDoc)
Database	   SQLite (development)
IDs	         UUID (all models)



API Endpoints

Endpoint	      Description

/api/users/	    User registration & management

/api/expenses/	CRUD expenses + budget summary

/api/plans/	    CRUD monthly budget plans

/api/plans/{id}/planitems/	CRUD category-level budget items (nested)

/api/auth/	    Djoser auth (login, token, etc.)

/swagger/	      Swagger UI documentation

/redoc/	        ReDoc documentation
