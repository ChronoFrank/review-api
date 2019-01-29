# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from .views import HelloView, UserReviewViewset
from .views import ReviewModelViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'reviews', ReviewModelViewSet)
router.register(r'users', UserReviewViewset)

urlpatterns = [
    url(r'^review/hello/$', HelloView.as_view(), name="hello"),
    url(r'^', include(router.urls)),
]
