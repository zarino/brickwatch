from django.views.generic import ListView

from catalog.models import CatalogSet


class CatalogSets(ListView):
    context_object_name = 'catalog_sets'

    def get_queryset(self):
        return CatalogSet.objects.all()
