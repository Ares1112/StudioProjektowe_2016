"""TOPR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from system_app.views import home_view, weather_view
from tourist_app.views import tourists_view
from system_app.api_views import api_get_routes, api_get_routes_info, api_get_weather_info
from tourist_app.api_views import api_get_tourists, api_get_tourist_danger_info, api_get_bears
from django.conf.urls.i18n import i18n_patterns

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = i18n_patterns(
    url(r'^admin/', admin.site.urls),


    url(r'^$', home_view, name='home_view'),
    url(r'^weather/$', weather_view, name='weather_view'),
    url(r'^tourists/$', tourists_view, name='tourists_view'),
    url(r'^api/get_routes_info/$', api_get_routes_info, name='api_get_routes_info'),
    url(r'^api/get_weather_info/$', api_get_weather_info, name='api_get_weather_info'),
    url(r'^api/get_tourist_danger_info/$', api_get_tourist_danger_info, name='api_get_tourist_danger_info'),

) + [url(r'^api/get_routes_kml/$', api_get_routes, name='api_get_routes'),
    url(r'^api/get_tourists_kml/$', api_get_tourists, name='api_get_tourists'),
    url(r'^api/get_bears_kml/$', api_get_bears, name='api_get_bears'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
	] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
