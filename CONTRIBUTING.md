How to contribute
=================

This document tells you how to get started contributing to the project - how to get your environment set up, what process to follow to get code in, how to get help, and what guidelines to use when you work.



About the application
---------------------

- Language: Python
- Web framework: Flask, with lots of plugins
- Deployment platform: Heroku
- Mail: Google Mail
- Database ORM: SQLAlchemy



Getting started
---------------

To set up your environment:

- Get the code: `git clone https://github.com/twinitialize/wolfstudy.git`
- Make a virtual environment: `virtualenv venv`
- Activate the virtual environment: `. venv/bin/activate`
- Install the required Python packages: `venv/bin/pip install -r requirements.txt`
- Run the web application locally: `python2 manage.py runserver`
- Go to `localhost:5000` in your browser to see if it works



Overview of the code
--------------------

- `manage.py` - contains management tools
- `config.py` - contains non-sensitive configuration for the application
- `.env` - (usually sensitive) environment variables related to the application (password, secret key, etc.)
- `tests/` - automated tests
- `wolfstudy/` - most of the code for the web application
    - `wolfstudy/auth/` - routes and forms related to authentication (login, registration, password resets, etc.)
    - `wolfstudy/main/` - routes and forms not related to the main application (homepage, question pages, etc.)
    - `wolfstudy/static/` - static files (CSS, JavaScript, images, etc.)
    - `wolfstudy/templates` - HTML templates related to the main application
    - `wolfstudy/templates/auth` - HTML templates related to authentication
    - `wolfstudy/templates/auth/email` - HTML and text templates for emails related to authentication
- `migrations` - contains database migration scripts
- `tmp/` - contains miscellaneous files (at the moment, HTML code coverage reports)



Working with the application
----------------------------

Using `manage.py`, you can run the application, test the code, work with the database, open a shell to work with the code, etc.

To use commands from `manage.py`, use the format:

    python2 manage.py <command>

Commands:
- `python2 manage.py runserver` - runs the web server locally at `localhost:5000`
- `python2 manage.py test` - runs the tests in the `tests` directory
- `python2 manage.py shell` - opens a Python shell with useful things imported (`app`, `db`, database models)
- `python2 manage.py db upgrade` - upgrades the current database to the most recent version using migration scripts in the `migrations/` directory
- `python2 manage.py db migrate -m "message"` - autogenerates a migration script based on database model changes - you must review this script to see if it was generated correctly (reflects all database model changes correctly)
- `python2 manage.py deploy` - performs the necessary functions to get the application ready to deploy (upgrades the database)



Getting work done
-----------------

A new feature or a bug is reported as an issue. Choose an issue to work on.

We currently use a feature-branch workflow in git. There is a 1:1 relationship between issues and feature branches. When adding a feature or fixing a bug, create and checkout a new branch with a descriptive name. Commit to that branch to implement the various parts of that feature or fix the bug.

Try out your new feature or test for the bug by running the web application locally. Write tests for your new feature or bug and run them.

When you've implemented the code, tested manually, and written tests, push the feature branch to GitHub and open a pull request. Do not merge the pull request until it has been reviewed.

When your feature branch has been merged into master, deploy the master branch to Heroku. Then make sure it works on Heroku.



How to generate a secret key
----------------------------

I'm not sure where else to put this.

    head -c 24 /dev/urandom > secret_key.txt
