from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.CatalogSets.as_view(template_name="catalog/sets.html"), name='catalog_sets'),
]
