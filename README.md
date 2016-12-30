# Brickwatch

A django project, for monitoring lego prices on ebay.

## Directory structure

By default, static files will be collected in `../public/`, and data will be saved into `../database.sqlite`, both *one level up* from the root of the git repo.

Perhaps you might want to organise your directories like so:

    ~/projects/brickwatch/
     |- database.sqlite
     |- public/
     |   `- static/
     `- src/ (<-- this is the git repo!)
         |- .git/
         |- .gitignore
         |- brickwatch/
         |   |- local_settings.py
         |   |- settings.py
         |   `- …etc
         |- catalog/
         |- manage.py
         `- …etc

## Set up

Assuming a directory structure as above:

    $ cd ~/projects/brickwatch
    $ git clone git@github.com:zarino/brickwatch.git src
    $ cd src
    $ virtualenv env
    (env)$ pip install -r requirements.txt
    (env)$ cp brickwatch/local_settings{.example,}.py

Then edit `brickwatch/local_settings.py` to include your ebay and brickset API credentials, and any other environment-specific changes you require.

For local development, you will want to compile the Sass files at `/static/sass` to CSS at `/static/css`:

    (env)$ sass --watch static/sass:static/css

(In production, you’ll want to compile the Sass files one-off, and then run `./manage.py collectstatic` to copy them into a directory that your webserver can serve up directly.)

## Run the site

    (env)$ ./manage.py runserver

## Apps

**market** – everything to do with ebay listings, active or ended.

**catalog** – everything to do with lego sets, like their names, RRPs, and production dates.
