# Brickwatch

A django project, for monitoring lego prices on ebay.

## Set up

    $ virtualenv env
    (env)$ pip install -r requirements.txt

Create a file at `brickwatch/local_settings.py` to override the default settings for your specific environment.


## Apps

**market** – everything to do with ebay listings, active or ended.

**catalog** – everything to do with lego sets, like their names, RRPs, and production dates.

<!--
**Model: catalog.Set**
- set_number (string, eg: 76040)
- set_number_variant (integer, eg: 1, from 76040-1)
- name (string)
- year (integer)
- availability (string)
- brickset_url (string)
- image_url (string)
- rrp_gbp (string, or DecimalField?)
- rrp_usd (string, or DecimalField?)
- rrp_eur (string, or DecimalField?)
-->
