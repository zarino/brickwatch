from __future__ import unicode_literals

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import dateparse

from decimal import Decimal

from lxml import etree
import pprint
import re
import requests

from catalog.models import CatalogSet

# Set up prettyprinter for debugging
pp = pprint.PrettyPrinter(indent=2)


class Command(BaseCommand):
    help = 'Import data for one or more Lego sets, from the Brickset API.'


    def add_arguments(self, parser):
        parser.add_argument(
            'set_number',
            nargs='+',
            type=str,
            help='a Lego set number, eg "20313-1". If the variant (the hyphen and final digit) are omitted, "-1" will automatically be appended to the supplied set number.',
        )


    def clean_set_number(self, set_number):
        if re.match(r'^\d{1,6}-\d{1,2}$', set_number):
            return set_number
        else:
            return '{}-1'.format(
                re.search(r'\d+', set_number).group()
            )


    def get_sets(self, query_params):
        params = {
            'apiKey': settings.BRICKSET_API_KEY,
            'userHash': settings.BRICKSET_USER_HASH,
            'setNumber': '',
            'query': '',
            'theme': '',
            'subtheme': '',
            'year': '',
            'owned': '',
            'wanted': '',
            'orderBy': '',
            'pageSize': '',
            'pageNumber': '',
            'userName': '',
        }
        params.update(query_params)
        response = requests.get('http://brickset.com/api/v2.asmx/getSets', params=params)

        # Remove namespaces from the XML, to make XPath simpler
        xml = re.sub(r'\sxmlns[^"]+"[^"]+"', '', response.content)

        # Lxml complains when the output of re.sub() is no longer an
        # unencoded byte string. So we make sure the string is encoded
        # to utf-8 (to match the xml doctype we get from the Brickset
        # API) and then tell lxml to parse it as utf-8.
        tree = etree.fromstring(
            xml.encode('utf-8'),
            parser=etree.XMLParser(encoding='utf-8')
        )

        return tree.xpath('//sets')


    def handle(self, *args, **options):
        # Users can specify multiple set numbers at the same time,
        # so we must handle each one in turn.
        for set_number in options['set_number']:
            set_number = self.clean_set_number(set_number)
            query_params = {
                'setNumber': set_number,
            }
            sets = self.get_sets(query_params)

            if len(sets) == 0:
                raise CommandError('Brickset API returned no results for {}'.format(query_params))
            elif len(sets) > 1:
                raise CommandError('Brickset API returned more than one result for {}'.format(query_params))

            set_details = {
                'set_number': set_number,
                'name': sets[0].xpath('//name')[0].text,
                'year': int(sets[0].xpath('//year')[0].text),
            }

            el = sets[0].xpath('//availability')
            if len(el) and el[0].text and el[0].text != '{Not specified}':
                set_details['availability'] = el[0].text

            url_tags = {
                'bricksetURL': 'brickset_url',
                'imageURL': 'image_url'
            }
            for api_tag_name, model_column_name in url_tags.iteritems():
                el = sets[0].xpath('//{}'.format(api_tag_name))
                if len(el) and el[0].text:
                    set_details[model_column_name] = el[0].text

            price_tags = {
                'UKRetailPrice': 'rrp_gbp',
                'USRetailPrice': 'rrp_usd',
                'EURetailPrice': 'rrp_eur',
            }
            for api_tag_name, model_column_name in price_tags.iteritems():
                el = sets[0].xpath('//{}'.format(api_tag_name))
                if len(el) and el[0].text:
                    set_details[model_column_name] = Decimal(el[0].text)

            # global pp
            # pp.pprint(set_details)

            s = CatalogSet(**set_details)
            s.save()
            self.stdout.write(self.style.SUCCESS(
                'Saved set {} {}'.format(
                    set_details['set_number'],
                    set_details['name'],
                )
            ))
