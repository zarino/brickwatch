from django.contrib import admin

from catalog.models import Set

@admin.register(Set)
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

