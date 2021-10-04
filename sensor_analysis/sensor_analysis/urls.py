"""sensor_analysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from . import views

urlpatterns = [
    path('admin', admin.site.urls),
    path('',views.indexPage,name="indexPage"),
    path('login',views.login_access,name='login'),
    path('home',views.homepage,name='home'),
    path('addUser', views.add_user, name='addUser'),
    path('addOrg', views.add_org, name='addOrg'),
    path('addNewOrg', views.add_new_org, name='addNewOrg')
]
