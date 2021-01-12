"""web_service_analyzer URL Configuration

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
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from analyzer import views as analayzer_views

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', analayzer_views.index, name='main'),
    path('analize_one/', analayzer_views.analize_one),
    path('analize_two/', analayzer_views.analize_two),
    path('result_analize_one', analayzer_views.result_analize_one),
    path('result_analize_two', analayzer_views.result_analize_two),
]

urlpatterns += staticfiles_urlpatterns()