"""my_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from custom_user.tools import auth
from rest_framework import permissions

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('custom_user.urls')),
    path('admin/', admin.site.urls),
    path('', include('my_app.urls'))
]

# Swagger UI documentation Automatic generated
schema_view = get_schema_view(
    openapi.Info(
        title="API documentation",
        default_version='0.1.3',
        description="Api documentation created by Nigar"
    ),
    # public=False,
    # authentication_classes=(auth.BasicAuthenticationNew,),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
