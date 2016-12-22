from django.contrib import admin

from market.models import Listing

def current_price(listing):
    return '{} {}'.format(
        listing.current_price,
        listing.current_price_currency
    )

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'listing_id',
        'title',
        current_price,
        'start_time',
        'end_time',
    )
    ordering = ('-end_time',)
