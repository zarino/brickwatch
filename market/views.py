from django.views.generic import ListView

from market.models import Listing


class Listings(ListView):
    context_object_name = 'listings'

    def get_queryset(self):
        return Listing.objects.filter(brickset_user=self.request.user)
