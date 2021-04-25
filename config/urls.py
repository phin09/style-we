from django.urls import path, include
from django.conf.urls import url

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('user', include('user.urls')),
    path('feed', include('feed.urls')),
    path('product', include('product.urls')),
]

# api documentation: drf-yasg 사용.
# 이를 위해 settings.py INSTALLED_APPS에 rest_framework와 drf_yasg를 추가하고
# django.contrib.admin와 django.contrib.auth 주석을 해제함.
schema_view = get_schema_view(
    openapi.Info(
        title="style-we API",
        default_version='v1.0.0',
        description="style-we project API document",
    ),
    validators=['flex'],
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    url(r'^swagger$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]