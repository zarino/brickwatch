from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Listings.as_view(template_name="market/listings.html"), name='market_listings'),
]
