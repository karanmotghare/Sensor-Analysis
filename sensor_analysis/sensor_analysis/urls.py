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
    path('logout',views.logout,name='logout'),
    path('sAdmin', views.sAdmin, name='sAdmin'),
    path('home',views.homepage,name='home'),
    path('addUser', views.add_user, name='addUser'),
    path('addOrg', views.add_org, name='addOrg'),
    path('addNewOrg', views.add_new_org, name='addNewOrg'),
    path('chartJS', views.chart_js, name='chart'),
    path('getSgAjax', views.getSgAjax, name='getSgAjax'),
    path('getSensorAjax', views.getSensorAjax, name='getSensorAjax'),
    path('getDataValues', views.getDataValues, name='getDataValues'),
    path('dataGen', views.dataGen, name='dataGen'),
    path('option_1_graph', views.option_1_graph, name='option_1_graph'),
    path('option_2_graph', views.option_2_graph, name='option_2_graph'),
    path('option_3_graph', views.option_3_graph, name='option_3_graph'),
    path('option_4_graph', views.option_4_graph, name='option_4_graph'),
    path('option_1_insert_db', views.option_1_insert_db, name='option_1_insert_db'),
    path('option_2_insert_db', views.option_2_insert_db, name='option_2_insert_db'),
    path('option_3_insert_db', views.option_3_insert_db, name='option_3_insert_db'),
    path('getStatistics', views.getStatistics, name='getStatistics'),
    path('getMotifs', views.getMotifs, name='getMotifs'),
    path('getADFT', views.getADFT, name='getADFT'),
    # path('getDataGen', views.data_Gen, name='getDataGen'),

]
