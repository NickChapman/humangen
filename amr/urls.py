from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^signup', signup, name='signup'),
    url(r'^signout', signout, name='signout'),
    url(r'^about', about, name='about'),
    url(r'^contact', contact, name='contact'),
    url(r'^.*', not_found, name='default'), # We render this if there are no matches
]
