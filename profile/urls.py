from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^edit/$', views.profile_edit, name='profile_edit'),
]
