from django.urls.conf import path
from requests.api import patch
from .views import *
urlpatterns = [
    path("crypto/", crypto, name="crypto")
    ]
