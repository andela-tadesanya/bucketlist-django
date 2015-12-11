![bucketlist logo](http://s27.postimg.org/fdhwsdoqr/Bucket_List_logo.png)

[![Coverage Status](https://coveralls.io/repos/andela-tadesanya/django-bucketlist-application/badge.svg?branch=master&service=github)](https://coveralls.io/github/andela-tadesanya/django-bucketlist-application?branch=master) [![Build Status](https://travis-ci.org/andela-tadesanya/django-bucketlist-application.svg)](https://travis-ci.org/andela-tadesanya/django-bucketlist-application)

# Introduction
A Django based application for creating and managing a bucketlist.

# FEATURES
- Supports multiple users
- Built with a postgres database
- Token, Session and Basic authentication supported
- Users can create multiple bucket lists and bucketlist items
- Users can edit/delete bucket lists and items in them

# INSTALLATION
- Download the repo
- cd into the project root in your favorite commandline tool
- Run `pip install -r requirements.txt` to install all dependencies
- Run `python bucketlist_django/manage_testing.py test bucketlist` to run tests
- Run `python bucketlist_django/manage_development makemigrations` and then run `python bucketlist_django/manage_development migrate` to create tables in the database
- Run `python bucketlist_django/manage_development runserver.py` to start the server
- On production run `python bucketlist_django/manage_production.py collectstatic` to collect static files
- On production use `manage_production.py` to run the server. Only use `manage_development.py` on development environment and `manage_testing.py` for testing.

*Note: Postgres User must be a superuser that can create a database or else test suites wont run*

# VERSION
version: 1.0.0

# API Documentation
Uses Django REST Swagger to document the API. Run the server and go to the URL 'api/v1.0/docs/'

# User Interface
There is also a user interface you can access to use the app
