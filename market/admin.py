from django.contrib import admin

from market.models import Listing, SetInAListing

def current_price(listing):
    return '{} {}'.format(
        listing.current_price,
        listing.current_price_currency,
    )

# http://stackoverflow.com/a/18108586
def sets_in_this_listing(self):
    return ', '.join([s.set_number for s in self.catalog_sets.all()])
sets_in_this_listing.short_description = "Set(s)"
sets_in_this_listing.allow_tags = True

class SetInListingInline(admin.TabularInline):
    model = SetInAListing
    verbose_name = "Sets in this listing"
    verbose_name_plural = "Sets in this listing"
    extra = 1

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'listing_id',
        'title',
        sets_in_this_listing,
        current_price,
        'start_time',
        'end_time',
        'is_active',
        'brickset_user',
    )

    ordering = ('-end_time',)

    list_display_links = (
        'listing_id',
        'title',
    )

    list_filter = (
        'sale_type',
        'condition',
        'brickset_user',
    )

    # https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#working-with-many-to-many-intermediary-models
    # http://stackoverflow.com/a/5948071
    inlines = (
        SetInListingInline,
    )

@admin.register(SetInAListing)
class SetInAListingAdmin(admin.ModelAdmin):
    pass