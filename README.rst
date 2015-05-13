pinkflamingo
===================

Below you will find basic setup and deployment instructions for the pinkflamingo project.

Mac setup
-------------------

System dependencies
~~~~~~~~~~~~~~~~~~~

Start by making sure you have these packages from `Homebrew <http://brew.sh/>`_
(``brew install`` them but really closely follow the Homebrew docs, *especially* for the databases):

* postgresql

Very first time
~~~~~~~~~~~~~~~~~~~

This setup assumes you have just cloned the git repo, have set up postgres, and are in the directory with this ``README.rst``::

    $ git pull origin master                                                                    # Pull master branch, syncs database, and migrates
    $ virtualenv ve --python=python2.7 --prompt="(pinkflamingo)"                                # Get a set of eggs just for this
    $ . ve/bin/activate                                                                         # Turn on the virtualenv
    $ pip install -r requirements/cpython2.txt                                                  # Fill the virtualenv with Python dependencies
    $ pip install -r requirements/development.txt                                               # Fill the virtualenv with development dependencies
    $ createuser -h localhost -p 5432 --createdb --no-createrole --no-superuser pinkflamingo    # Create a database user in postgres
    $ createdb -h localhost -p 5432 -E utf8 -O pinkflamingo pinkflamingo                        # Create the main pinkflamingo database in postgres
    $ cp pinkflamingo/settings/local/dev.py.example pinkflamingo/settings/local/dev.py          # Your dev.py is your personal settings. Edit them later.
    $ cp pinkflamingo/settings/local/tests.py.example pinkflamingo/settings/local/tests.py      # Your dev.py is your personal settings. Edit them later.
    $ python manage.py migrate                                                                  # Migrate the DB
    $ python manage.py loaddata initial_data_MANUAL                                             # Create initial data for the project
    $ python manage.py createsuperuser                                                          # Establish an admin so you can log in

You should now be able to run the development server::

    python manage.py runserver

You should also install test dependencies and run the test suite::

    pip install -r requirements/tests.txt
    tox api pinkflamingo (or python manage.py test api pinkflamingo)

To generate random ratings on all books from all users, use the following management command.
Note that this is destructive (it will delete all existing ratings)::

    python manage.py generate_random_ratings

The tasks
-------------------

1. Build an endpoint for creating user ratings on books
2. Build an endpoint for returning all books by a specific author
3. Add an average_rating field that comes back from GET requests on books (both list and detail endpoints are fine)
