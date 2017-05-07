from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^signup', signup, name='signup'),
    url(r'^signout', signout, name='signout'),
    url(r'^contact', contact, name='contact'),
    url(r'^easy_generate', easy_generate, name='easy_generate'),
    url(r'^generate', generate, name='generate'),
    url(r'^get_data', get_sentence_pairs, name='get_data'),
    url(r'^.*', not_found, name='default'), # We render this if there are no matches
]
