# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import HelloView

urlpatterns = [
    url(r'^review/hello/$', HelloView.as_view(), name="hello"),
]