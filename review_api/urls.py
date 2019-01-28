# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework_simplejwt import views as jwt_views
from review_api.review import urls as review_urls
from django.contrib import admin

admin.site.site_header = 'Review Api'
admin.site.site_title = admin.site.site_header
admin.site.site_url = None

api_v1 = [
    url(r'^api/v1/access_token/$', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/v1/refresh_token/$', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^api/v1/', include(review_urls))
]

urlpatterns = [
    url(r'^admin/', include(admin.site.urls), name='root'),
] + api_v1
