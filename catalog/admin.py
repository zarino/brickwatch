from django.contrib import admin

from catalog.models import CatalogSet
from market.models import SetInAListing

class ListingsWithSet(admin.TabularInline):
    model = SetInAListing
    verbose_name = "Listings with this set"
    verbose_name_plural = "Listings with this set"
    extra = 1

@admin.register(CatalogSet)
class SetAdmin(admin.ModelAdmin):
    list_display = (
        'admin_thumbnail',
        'set_number',
        'name',
        'year',
    )

    list_display_links = (
        'admin_thumbnail',
        'set_number',
        'name',
    )

    list_filter = (
        'year',
        'availability',
    )

    inlines = (
        ListingsWithSet,
    )

