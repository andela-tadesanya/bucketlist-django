![bucketlist logo](http://s11.postimg.org/5kbbghv2n/bucketlistlogo.jpg)

[![Coverage Status](https://coveralls.io/repos/andela-tadesanya/django-bucketlist-application/badge.svg?branch=master&service=github)](https://coveralls.io/github/andela-tadesanya/django-bucketlist-application?branch=master) [![Build Status](https://travis-ci.org/andela-tadesanya/django-bucketlist-application.svg)](https://travis-ci.org/andela-tadesanya/django-bucketlist-application)

# Introduction
A Django based application for creating and managing a bucketlist.

# Features
- Supports multiple users
- Built with a postgres database
- Token, Session and Basic authentication supported
- Users can create multiple bucket lists and bucketlist items
- Users can edit/delete bucket lists and items in them

# Installation
- Download the repo
- cd into the project root in your favorite commandline tool
- Run `pip install -r requirements.txt` to install all dependencies
- Create an environment variable `DJANGO_ENVIRONMENT` with the value 'development', 'production', or 'testing' depending on the environment
- Run `python bucketlist_django/manage.py test bucketlist` to run tests, with the environment variable DJANGO_ENVIRONMENT set to 'testing'
- Run `python bucketlist_django/manage.py makemigrations` and then run `python bucketlist_django/manage.py migrate` to create tables in the database
- Run `python bucketlist_django/manage.py runserver` to start the server
- On production run `python bucketlist_django/manage.py collectstatic` to collect static files
- On production set the environment variable DJANGO_ENVIRONMENT to 'production'.

*Note: Postgres User must be a superuser that can create a database or else test suites wont run*

# Version
version: 1.0.0

# API Documentation
Uses Django REST Swagger to document the API. Run the server and go to the URL `api/v1/docs/`
*You need to be logged in to get full access to the swagger documentation*

# API Authentication
The API uses tokens to authenticate, send a post request to the url `/api/v1/token/` with the parameters 'username' and 'password'

# User Interface
There is also a user interface you can access to use the app from the root URL

# Demo
[https://django-bucketlist-application.herokuapp.com/](https://django-bucketlist-application.herokuapp.com/)

# Credit
God, Google and Me
