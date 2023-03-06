# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

     # Transactions
    path("collections/", views.collections_index, name="collections_index"),

    # scancard
    path("scancard/", views.scancard, name="scancard"),

    # Showcard
    path("showcard/<int:id>", views.showcard, name="showcard"),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
   


]
