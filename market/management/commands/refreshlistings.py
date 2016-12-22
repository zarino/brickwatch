from __future__ import unicode_literals

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import dateparse

from decimal import Decimal

# https://github.com/timotheus/ebaysdk-python/wiki/Trading-API-Class
from ebaysdk.trading import Connection
from ebaysdk.exception import ConnectionError

import pprint

from market.models import Listing

class Command(BaseCommand):
    help = 'Fetches the latest watchlist ("MyeBayBuying") data from eBay'

    def query(self, *args):
        try:
            api = Connection(
                config_file=None,
                appid=settings.EBAY_APP_ID,
                devid=settings.EBAY_DEV_ID,
                certid=settings.EBAY_CERT_ID,
                token=settings.EBAY_TOKEN,
            )
            response = api.execute(*args)
            return response.dict()
        except ConnectionError as e:
            return e.response.dict()

    def handle(self, *args, **options):
        # Set up prettyprinter for debugging
        pp = pprint.PrettyPrinter(indent=2)

        results = self.query('GetMyeBayBuying', {
            'WatchList': {
                'Include': True
            }
        })

        # pp.pprint(results)

        if 'Errors' in results:
            raise CommandError('eBay API {} {}: {} {}'.format(
                results['Errors']['ErrorClassification'],
                results['Errors']['ErrorCode'],
                results['Errors']['ShortMessage'],
                results['Errors']['LongMessage'],
            ))

        elif 'WatchList' in results:
            for item in results['WatchList']['ItemArray']['Item']:
                listing_details = {
                    'listing_id': item['ItemID'],
                    'listing_url': item['ListingDetails']['ViewItemURL'],
                    'title': item['Title'],
                    # 'condition': ,
                    'start_time': dateparse.parse_datetime(
                        item['ListingDetails']['StartTime']
                    ),
                    'end_time': dateparse.parse_datetime(
                        item['ListingDetails']['EndTime']
                    ),
                    'seller_user_id': item['Seller']['UserID'],
                }

                if item['ListingType'] == 'Chinese':
                    listing_details['sale_type'] = Listing.SALE_TYPE_AUCTION
                elif item['ListingType'] == 'FixedPriceItem':
                    listing_details['sale_type'] = Listing.SALE_TYPE_BUYITNOW
                else:
                    self.stdout.write(self.style.SUCCESS(
                        'Skipping item {}: unknown ListingType "{}"'.format(
                            item['ItemID'],
                            item['ListingType'],
                        )
                    ))
                    continue

                if 'BuyItNowPrice' in item:
                    listing_details['buyitnow_price'] = Decimal(item['BuyItNowPrice']['value'])
                    listing_details['buyitnow_price_currency'] = item['BuyItNowPrice']['_currencyID']

                if 'ShippingDetails' in item:
                    listing_details['shipping_cost'] = Decimal(item["ShippingDetails"]["ShippingServiceOptions"]["ShippingServiceCost"]["value"])
                    listing_details['shipping_cost_currency'] = item["ShippingDetails"]["ShippingServiceOptions"]["ShippingServiceCost"]["_currencyID"]

                if 'SellingStatus' in item:
                    if 'CurrentPrice' in item['SellingStatus']:
                        listing_details['current_price'] = Decimal(item['SellingStatus']['CurrentPrice']['value'])
                        listing_details['current_price_currency'] = item['SellingStatus']['CurrentPrice']['_currencyID']
                    if 'BidCount' in item['SellingStatus']:
                        listing_details['bid_count'] = item['SellingStatus']['BidCount']

                if 'StartPrice' in item:
                    listing_details['start_price'] = Decimal(item['StartPrice']['value'])
                    listing_details['start_price_currency'] = item['StartPrice']['_currencyID']

                # pp.pprint(listing_details)

                listing = Listing(**listing_details)
                listing.save()
                self.stdout.write(self.style.SUCCESS(
                    'Saved item {} {}'.format(
                        item['ItemID'],
                        item['Title'],
                    )
                ))

            # self.stdout.write(self.style.SUCCESS('Yay! Listings!'))
