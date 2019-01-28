# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import HelloView, UserReviewSingUp

urlpatterns = [
    url(r'^review/hello/$', HelloView.as_view(), name="hello"),
    url(r'^review/singup/$', UserReviewSingUp.as_view(), name='signup'),
]
