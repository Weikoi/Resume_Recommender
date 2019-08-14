#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.staticfiles import views as static_views
from django.conf.urls.static import static
from django.conf import settings
import webapp.views as views

urlpatterns = [
                  url(r'^$', views.index, name='index'),
                  url(r'analysis/', views.analysis, name='analysis'),
                  url(r'result/', views.result, name='result'),
                  url(r'about/', views.about, name='about'),
                  url(r'statistics/', views.statistics, name='statistics'),
                  url(r'cv_list/', views.cv_list, name='cv_list'),
]