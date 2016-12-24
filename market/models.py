# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from catalog.models import CatalogSet

@python_2_unicode_compatible
class Listing(models.Model):
    SALE_TYPE_AUCTION = 0
    SALE_TYPE_BUYITNOW = 1
    SALE_TYPE_CHOICES = (
        (SALE_TYPE_AUCTION, 'Auction'),
        (SALE_TYPE_BUYITNOW, 'BuyItNow'),
    )
    # http://pages.ebay.com/help/sell/item-condition.html#collectibles
    CONDITION_USED = 0
    CONDITION_NEW = 1
    CONDITION_CHOICES = (
        (CONDITION_USED, 'Used'),
        (CONDITION_NEW, 'New'),
    )
    listing_id = models.CharField(max_length=32, primary_key=True)
    listing_url = models.URLField(max_length=512)
    title = models.CharField(max_length=256)
    sale_type = models.IntegerField(default=0, choices=SALE_TYPE_CHOICES, null=True)
    condition = models.IntegerField(default=0, choices=CONDITION_CHOICES, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    seller_user_id = models.CharField(max_length=64)

    catalog_sets = models.ManyToManyField(CatalogSet, through='SetInAListing')

    bid_count = models.IntegerField(default=0, null=True)
    start_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    start_price_currency = models.CharField(max_length=3, null=True)
    current_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    current_price_currency = models.CharField(max_length=3, null=True)
    shipping_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    shipping_cost_currency = models.CharField(max_length=3, null=True)

    buyitnow_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    buyitnow_price_currency = models.CharField(max_length=3, null=True)

    def __str__(self):
        return '{} {}'.format(
            self.listing_id,
            self.title,
        )

    @property
    def is_active(self):
        return self.end_time > timezone.now()

@python_2_unicode_compatible
class SetInAListing(models.Model):
    catalog_set = models.ForeignKey(CatalogSet, on_delete=models.CASCADE)
    market_listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    number = models.IntegerField(default=1, help_text="How many of this set are in this listing?")

    class Meta:
        verbose_name = 'Set in a listing'
        verbose_name_plural = 'Sets in listings'

    def __str__(self):
        return '{} (×{}) in listing {}'.format(
            self.catalog_set.set_number,
            self.number,
            self.market_listing.listing_id,
        )
