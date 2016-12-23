# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Set(models.Model):
    set_number = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=128)
    year = models.IntegerField(default=0, null=True)
    availability = models.CharField(max_length=64, null=True)
    brickset_url = models.URLField(max_length=512, null=True)
    image_url = models.URLField(max_length=512, null=True)
    rrp_gbp = models.DecimalField('UK RRP (£)', max_digits=6, decimal_places=2, null=True)
    rrp_usd = models.DecimalField('US RRP ($)', max_digits=6, decimal_places=2, null=True)
    rrp_eur = models.DecimalField('EU RRP (€)', max_digits=6, decimal_places=2, null=True)

    def __str__(self):
        return '{} {}'.format(self.set_number, self.name)

    def admin_thumbnail(self):
        return '<img src="{}" width="100" style="height: auto" />'.format(
            self.image_url
        )

    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True
