
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

sw='swagger/'
SchemaView = get_schema_view(
    openapi.Info(
        title="AREZ API",
        default_version='3.0.0',
    ),
    public=False,
    permission_classes=([permissions.IsAuthenticated])
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),


    path(sw, SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]

  

