# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import HelloView, UserReviewSingUpView, ReviewModelView

urlpatterns = [
    url(r'^review/hello/$', HelloView.as_view(), name="hello"),
    url(r'^review/user/$', UserReviewSingUpView.as_view(), name='user'),
    url(r'^review/', ReviewModelView.as_view(), name='reviews'),
]
