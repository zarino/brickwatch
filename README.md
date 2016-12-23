# Brickwatch

A django project, for monitoring lego prices on ebay.

## Set up

    $ virtualenv env
    (env)$ pip install -r requirements.txt

Create a file at `brickwatch/local_settings.py` to override the default settings for your specific environment.


## Apps

**market** – everything to do with ebay listings, active or ended.

**catalog** – everything to do with lego sets, like their names, RRPs, and production dates.
